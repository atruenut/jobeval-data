# Pack specification (schema 1, engine 1.0)

A **pack** is a data-only description of one jurisdiction layer: tax brackets,
contribution formulas, statutory minimums, and (later) benefit programs. The engine
(`evalcore` in the app repo) knows nothing about any country. Everything it computes
comes from a *bundle*: a pack merged with its `extends` chain.

Packs are authored in YAML under `packs-src/`, compiled to canonical JSON by
`tools/build.py`, validated and tested by `eval-cli`, and published with a signed
catalog (`index.json`).

## Principles

- **Parameters are data, rules are logic.** Yearly numbers live in `parameters`; rules
  only reference them with `$name`. A routine tax-year update is a parameters-only diff.
- **Total language.** Rules are pure expressions over a dependency graph. No loops,
  recursion, user functions, or I/O, so every pack evaluates in bounded time.
- **Exact arithmetic.** Fixed-point decimals (9 places). Numbers are kept as the text
  the author wrote. A value with more than 9 decimal places is an error, not a rounding.
- **Everything is cited.** Every parameter names a source; sources carry an authority
  level. The evaluator records a trace (rule, expression, inputs read, result).
- **Honest coverage.** `tier` says how much is modelled; `not_modelled` lists what isn't.

## Top-level fields

| Field | Required | Notes |
|---|---|---|
| `schema` | yes | `1` |
| `id` | yes | Unique, e.g. `CA-NB-2026` |
| `kind` | yes | `country`, `subregion`, or `locality` |
| `extends` | non-country | Parent pack id |
| `region` | yes | `{ country, subregion? }` |
| `valid` | yes | `{ from, to? }` as `YYYY-MM-DD`, inclusive |
| `revision` | yes | Integer, bumped on every published change |
| `tier` | yes | `estimate`, `partial`, or `full` (see below) |
| `currency` | country packs | ISO 4217; children inherit |
| `requires_engine` | no | `">=MAJOR.MINOR"`. Older apps skip the pack and say to update |
| `labels` | no | Display names by language |
| `sources` | yes | `id -> { authority, title?, url?, retrieved? }` (title or url required) |
| `parameters` | no | See below |
| `inputs` | no | Values the app supplies: `name -> { type, label?, default? }` |
| `rules` | no | List of `{ id, expr, label?, note?, public? }` |
| `outputs` | no | Named slots: `slot -> [rule ids]` (child packs use `append`) |
| `append` | no | Adds rules to a parent's slot |
| `replace` | no | Ids deliberately overriding a parent's rule/parameter/input/slot |
| `statutory` | no | `name -> expression`; becomes rule `statutory.<name>` |
| `not_modelled` | no | Free-text list of known gaps |
| `programs` | no | Reserved (benefit programs); carried through, not yet evaluated |

### Sources and authority

`authority` is `official`, `official_secondary` (a regulator's secondary publication),
or `third_party`. Third-party figures may bootstrap a draft but need confirmation.

### Parameters

```yaml
parameters:
  cpp:                       # static value (number, string, object, or table)
    source: cra_cpp
    value: { rate: 0.0595, exemption: 3500 }
  min_wage:                  # effective-dated: value in force on the evaluation date wins
    effective:
      - { from: 2025-04-01, value: 15.65, source: gnb_minwage }
      - { from: 2026-04-01, value: 15.90, source: gnb_minwage }
```

Dated parameters need an `as_of` date at evaluation time; a date before the first entry
is an error. Entries must be in strictly ascending `from` order.

### Tiers

| Tier | Meaning | Enforced by the validator |
|---|---|---|
| `estimate` | Generic or rough | nothing |
| `partial` | Tax and contributions modelled; known gaps listed | nothing |
| `full` | Everything relevant modelled and verified | `not_modelled` must be empty; every parameter must have an `official`/`official_secondary` source |

A bundle's tier is the weakest in its extends chain.

### Layering

- A child pack may **add** rules, parameters, inputs, and sources.
- It may not silently shadow a parent's. Overriding needs the id listed under `replace`
  (the validator warns if a `replace` entry overrides nothing).
- `append: { income_tax: [nb.tax] }` extends a parent's output slot; `outputs` on a
  child *replaces* a slot and therefore needs `replace`.
- Currency must match the parent's.
- A rule id may not equal an input name.

## Rule language

```
expr    := or
or      := and ("or" and)*
and     := not ("and" not)*
not     := "not" not | cmp
cmp     := sum (("<"|"<="|">"|">="|"=="|"!=") sum)?
sum     := prod (("+"|"-") prod)*
prod    := unary (("*"|"/") unary)*
unary   := "-" unary | primary
primary := number | "string" | true | false | name | $param.path | @slot
         | fn "(" args ")" | "(" expr ")"
```

- `name`: a dotted rule id or input (`cpp.base`, `gross_annual`).
- `$a.b.c`: a parameter. The longest prefix naming a parameter wins; the rest indexes
  into its value (`$cpp.rate` is field `rate` of parameter `cpp`).
- `@slot`: the sum of the rules in an output slot across all loaded layers.
- Comparison is non-associative (`a < b < c` is a syntax error). `==` and `!=` work on
  any matching types; ordering needs numbers. Mixing types is an error, never coerced.
- Division by zero is an error.

### Functions

| Function | Meaning |
|---|---|
| `min(a, b, ...)`, `max(a, b, ...)` | |
| `clamp(x, lo, hi)` | `min(max(x, lo), hi)`; error if `hi < lo` |
| `abs`, `floor`, `ceil` | |
| `round(x [, step [, mode]])` | Default step `0.01`, mode `half_up`. Modes: `half_up`, `half_even`, `down`, `up`, `floor`, `ceil` |
| `if(cond, a, b)` | Lazy: only the chosen branch is evaluated |
| `bracket(base, table)` | Marginal schedule. `table`: rows `{ up_to, rate }`, last row without `up_to`. Values at or below 0 give 0 |
| `tier_lookup(key, table)` | Step lookup. Rows `{ up_to, value }`; `up_to` inclusive; last row open |
| `phase_down(x, params)` | Linear reduction from `max` at `from` to `min` at `to` (e.g. the federal basic personal amount) |
| `phase_out(credit, x, start, rate)` | `max(0, credit - rate * max(0, x - start))` |

Anything beyond this set is a new primitive (an engine minor-version bump), never a
workaround inside a pack.

## Validation (`eval-cli validate`)

Errors: bad schema or fields, unparseable expressions, unknown references (rule, input,
parameter, slot), dependency cycles, id collisions with a parent, unknown sources,
currency mismatch, `requires_engine` newer than the engine, tier violations.
Warnings: rules never used by a slot or another rule (mark `public: true` for rules
meant only to be queried by the UI or tests), unused parameters, no-op `replace`.

## Golden tests

```yaml
suite: CA-NB-2026
pack: CA-NB-2026
tolerance: { abs: 0.01 }
cases:
  - id: cpp-ei-mid-50k
    status: derived            # official | derived | pending
    inputs: { gross_annual: 50000, as_of: 2026-11-10 }
    expect: { cpp.base: 2766.75, "@contributions": 3581.75 }
```

- `official`: value taken from an official calculator run (record inputs and date).
- `derived`: independent arithmetic from published parameters. Catches wiring errors,
  not misreadings of the law.
- `pending`: awaiting a reference value. Skipped, never counted as passed.
- An `expect` key is a rule id, or `@slot`. A `null` value skips that key.
- Put cases at boundaries: each bracket edge, caps, phase-out bands, effective dates.

## Build and publish

```
python3 tools/build.py compile      # YAML -> dist/packs/<id>-r<rev>.<hash8>.json, dist/tests/*.json
eval-cli validate dist/packs
eval-cli test --packs dist/packs dist/tests
python3 tools/build.py manifest     # dist/index.json
```

`index.json` lists every pack with its hash, size, tier, validity window,
`requires_engine`, and last-verified date. In CI the catalog is signed with minisign
(`index.json.minisig`); the app embeds the public key and verifies the catalog, then each
pack against the catalog's SHA-256.

## Versioning

- Pack: `id` + integer `revision` (any published change bumps it).
- Schema: integer (`schema: 1`); a breaking change gets a new number.
- Engine: `MAJOR.MINOR`. New primitives bump MINOR; packs using them declare
  `requires_engine`.
