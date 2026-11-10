# Official calculator runs needed

To promote the Canada/New Brunswick pack from `derived` tests to `official` ones, run the
CRA **Payroll Deductions Online Calculator** (PDOC) and record the results below.

Settings for every run: province **New Brunswick**, pay period **biweekly (26)**, year
**2026**, **single**, default TD1 (basic personal amounts only), employment income only,
no other deductions.

Gross annual salaries to run (they sit on the boundaries that matter):

| Gross annual | Why |
|---|---|
| 20,000 | Low income, well below the first bracket edges |
| 35,000 | Mid-low |
| 50,000 | Typical; first NB bracket edge is 52,333 |
| 68,900 | EI maximum insurable earnings |
| 74,600 | CPP ceiling (YMPE) |
| 80,000 | Inside the CPP2 band |
| 85,000 | CPP2 ceiling (YAMPE) |
| 120,000 | Above all CPP/EI caps; third federal bracket |
| 200,000 | Inside the federal basic-personal-amount phase-down band |

For each run record: gross, federal tax, provincial tax, CPP, CPP2, EI, and the date and
pay-period assumptions. The calculator works per pay period, so multiply by 26 and expect
differences of a few cents to a few dollars from rounding and from credits this pack does
not yet model (see `not_modelled` in the packs).

| Gross annual | Fed tax / period | NB tax / period | CPP / period | CPP2 / period | EI / period | Run date |
|---|---|---|---|---|---|---|
| | | | | | | |
