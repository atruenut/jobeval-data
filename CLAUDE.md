# jobeval-data

Data repo for the job evaluator. Read `docs/PACK_SPEC.md` before touching packs.

- Yearly changes are parameter edits, never rule logic. New logic means a new engine
  primitive in jobeval-app, with `requires_engine` bumped here.
- Every parameter needs a `source`; never invent figures. Trustable third-party sources (e.g. Tax Foundation) are accepted when labelled `authority: third_party`; unverified values stay out, or
  the pack stays `partial` with the gap in `not_modelled`.
- Test expectations marked `official` must come from an official calculator run with the
  inputs and date recorded. Tax-line expectations without a reference stay `pending`.
- Check locally: `python3 tools/build.py compile && eval-cli validate dist/packs &&
  eval-cli test --packs dist/packs dist/tests` (eval-cli is built from jobeval-app).
- Never commit key material. Signing uses the `PACK_SIGNING_KEY` Actions secret only.
