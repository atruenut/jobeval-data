#!/usr/bin/env python3
"""Compile pack and test sources (YAML) into canonical JSON, and build the catalog.

  tools/build.py compile [--out dist]     YAML -> dist/packs/*.json, dist/tests/*.json
  tools/build.py manifest [--out dist]    dist/index.json (hashes, sizes, metadata)

Numbers are kept as the exact text the author wrote ("0.0595", "15.90"); they never
pass through binary floats. The expression language and all rule semantics live in
the C++ engine (`eval-cli validate`), not here: this script only transcodes.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REVISION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class RawNum(str):
    """A YAML number, kept as its original text."""


class Loader(yaml.SafeLoader):
    pass


# Strict YAML 1.2-style scalars: only true/false are booleans (so country code NO
# stays a string), dates stay strings, numbers keep their source text.
Loader.yaml_implicit_resolvers = {
    k: [(t, r) for (t, r) in v if t not in ("tag:yaml.org,2002:bool", "tag:yaml.org,2002:timestamp")]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), list("tf"))
Loader.add_implicit_resolver("tag:yaml.org,2002:int", re.compile(r"^-?(?:0|[1-9][0-9]*)$"), list("-0123456789"))
Loader.add_implicit_resolver(
    "tag:yaml.org,2002:float", re.compile(r"^-?(?:0|[1-9][0-9]*)\.[0-9]+(?:[eE][-+]?[0-9]+)?$"), list("-0123456789")
)


def _construct_num(loader, node):
    return RawNum(node.value)


def _construct_bool(loader, node):
    return node.value == "true"


Loader.add_constructor("tag:yaml.org,2002:int", _construct_num)
Loader.add_constructor("tag:yaml.org,2002:float", _construct_num)
Loader.add_constructor("tag:yaml.org,2002:bool", _construct_bool)


def _no_duplicate_keys(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys)


def dump(value) -> str:
    """Canonical compact JSON, number text preserved, key order preserved."""
    if isinstance(value, RawNum):
        return str(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(str(k), ensure_ascii=False) + ":" + dump(v) for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(dump(v) for v in value) + "]"
    raise TypeError(f"unsupported value in source: {value!r} ({type(value).__name__})")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.load(f, Loader=Loader)


def cmd_compile(out: Path) -> int:
    packs_out = out / "packs"
    tests_out = out / "tests"
    packs_out.mkdir(parents=True, exist_ok=True)
    tests_out.mkdir(parents=True, exist_ok=True)
    for stale in list(packs_out.glob("*.json")) + list(tests_out.glob("*.json")):
        stale.unlink()
    errors = 0
    seen_ids = {}
    for src in sorted((ROOT / "packs-src").rglob("*.yaml")):
        try:
            doc = load_yaml(src)
        except yaml.YAMLError as e:
            print(f"error: {src.relative_to(ROOT)}: {e}", file=sys.stderr)
            errors += 1
            continue
        pid, rev = doc.get("id"), doc.get("revision")
        if not isinstance(pid, str) or not REVISION_RE.match(pid) or not isinstance(rev, RawNum):
            print(f"error: {src.relative_to(ROOT)}: needs a valid string 'id' and numeric 'revision'", file=sys.stderr)
            errors += 1
            continue
        if pid in seen_ids:
            print(f"error: {src.relative_to(ROOT)}: id {pid} also defined in {seen_ids[pid]}", file=sys.stderr)
            errors += 1
            continue
        seen_ids[pid] = src.relative_to(ROOT)
        body = dump(doc) + "\n"
        digest = hashlib.sha256(body.encode()).hexdigest()[:8]
        (packs_out / f"{pid}-r{rev}.{digest}.json").write_text(body, encoding="utf-8", newline="\n")
        print(f"compiled {src.relative_to(ROOT)} -> {pid}-r{rev}.{digest}.json")
    for src in sorted((ROOT / "tests-src").rglob("*.yaml")):
        try:
            doc = load_yaml(src)
        except yaml.YAMLError as e:
            print(f"error: {src.relative_to(ROOT)}: {e}", file=sys.stderr)
            errors += 1
            continue
        (tests_out / (src.stem + ".json")).write_text(dump(doc) + "\n", encoding="utf-8", newline="\n")
        print(f"compiled {src.relative_to(ROOT)}")
    return 1 if errors else 0


def cmd_manifest(out: Path) -> int:
    entries = []
    for path in sorted((out / "packs").glob("*.json")):
        data = path.read_bytes()
        doc = json.loads(data)
        retrieved = sorted(
            s["retrieved"] for s in doc.get("sources", {}).values() if isinstance(s.get("retrieved"), str)
        )
        entries.append(
            {
                "id": doc["id"],
                "kind": doc["kind"],
                "extends": doc.get("extends"),
                "country": doc["region"]["country"],
                "subregion": doc["region"].get("subregion"),
                "labels": doc.get("labels", {}),
                "tier": doc["tier"],
                "revision": int(doc["revision"]),
                "valid_from": doc["valid"]["from"],
                "valid_to": doc["valid"].get("to"),
                "requires_engine": doc.get("requires_engine", ">=1.0"),
                "last_verified": retrieved[-1] if retrieved else None,
                "file": "packs/" + path.name,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            }
        )
    manifest = {
        "catalog": 1,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packs": entries,
    }
    (out / "index.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"manifest: {len(entries)} pack(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["compile", "manifest"])
    ap.add_argument("--out", default=str(ROOT / "dist"))
    args = ap.parse_args()
    out = Path(args.out)
    return cmd_compile(out) if args.command == "compile" else cmd_manifest(out)


if __name__ == "__main__":
    sys.exit(main())
