# Contributing to jobeval-data

Read `docs/PACK_SPEC.md` first and `CLAUDE.md` for the rules. The app that consumes this
data is [jobeval-app](https://github.com/atruenut/jobeval-app); see its `docs/ARCHITECTURE.md`.

## Rules

1. **Every parameter needs a `source`.** Prefer the official publication (cite title, url,
   retrieved date). Never invent or estimate a figure; leave it out and list the gap in
   `not_modelled` (the pack then stays `partial`).
2. **Yearly changes are parameter edits.** If a rule needs new logic, that is a new engine
   primitive in jobeval-app plus `requires_engine` here.
3. **Bump `revision`** whenever a pack's content changes.
4. **Tests.** Cases marked `official` must come from an official calculator run with inputs
   and date recorded (`docs/OFFICIAL_RUNS.md`). `derived` cases come from an independent
   implementation (see `tools/reference_ca_nb.py`), not from the pack itself. Tax-line
   expectations with no reference stay `pending`.
5. Never commit key material; signing uses the `PACK_SIGNING_KEY` Actions secret only.

## Adding a region

1. Copy the nearest layer in `packs-src/` (country layer first, then subregions that
   `extends` it).
2. Fill parameters from official sources; write rules; use the standard slot names.
3. Write an independent reference script or official runs and add golden tests.
4. Check locally (needs `eval-cli` built from jobeval-app):

```
python3 tools/build.py compile
eval-cli validate dist/packs
eval-cli test --packs dist/packs dist/tests
```

5. Open a PR; CI repeats the checks. Merging to `main` signs and publishes the catalog.

## Known upcoming changes

- Canada 2027: Bill C-30 reportedly lowers the CPP rate from 9.9% to 9.5% (base 4.95% to
  4.75%) from 2027-01-01. Unverified against official CRA tables; do not enter until the
  2027 CRA figures are published.
