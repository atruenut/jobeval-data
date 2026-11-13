# jobeval-data

Jurisdiction data packs for the job-opportunity evaluator: income tax, social
contributions, statutory employment minimums and (later) benefit programs, per region
and tax year. The desktop app ([jobeval-app](https://github.com/atruenut/jobeval-app))
downloads only the packs a user selects and caches them for offline use.

| Path | Contents |
|---|---|
| `packs-src/` | Pack sources (YAML), one file per jurisdiction layer and year |
| `tests-src/` | Golden-test suites (YAML) checking packs against official calculators or derived arithmetic |
| `tools/build.py` | Compiles YAML to canonical JSON and builds the signed catalog input |
| `docs/PACK_SPEC.md` | The pack format and rule language |
| `CONTRIBUTING.md` | How to add or change packs |
| `docs/OFFICIAL_RUNS.md` | Official calculator runs still needed to promote `derived` tests |
| `.engine-ref` | Engine version (a ref of jobeval-app) that CI validates against |

## Workflow

```
pip install -r tools/requirements.txt
python3 tools/build.py compile                       # -> dist/
eval-cli validate dist/packs                         # eval-cli is built from jobeval-app
eval-cli test --packs dist/packs dist/tests
python3 tools/build.py manifest                      # -> dist/index.json
```

CI does the same on every push and pull request. Merging to `main` signs the catalog
(`PACK_SIGNING_KEY`, optionally `PACK_SIGNING_PASSWORD`) and publishes `index.json`,
`index.json.minisig` and `packs/` to GitHub Pages.

## Updating for a new tax year

1. Copy last year's pack to the new year; change `id`, `valid`, `revision`, and the
   `retrieved` dates.
2. Update `parameters` from the official sources (rules should not need to change).
3. Add or adjust golden cases at the new boundaries; record official calculator results.
4. Open a pull request; CI shows validation and test results.

## Coverage

Each pack declares a `tier` (`estimate`, `partial`, `full`) and lists what it does not
model under `not_modelled`. Figures here are estimates for decision support, not
payroll-grade results.

## Licence

Data and documentation: CC BY 4.0. Scripts in `tools/`: MIT (`LICENSE-CODE`). See `LICENSE`.
