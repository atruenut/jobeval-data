# Coverage (2026)

All Canadian packs extend `CA-2026` (federal tax, CPP/CPP2, EI) and are tier `partial`: they
compute as if the job were the person's only income for a full tax year, with the basic personal
amount, CPP/EI credits and the Canada employment amount; other credits are in `not_modelled`.
Provincial tax comes from CRA T4127 (122nd ed.), chapter 8 tables; Ontario surtax, health
premium and tax reduction from CRA T4032ON (Jan 2026). Tests are `derived` from
`tools/reference_ca_nb.py` / `tools/reference_ca_provinces.py` until official calculator runs are
recorded (`docs/OFFICIAL_RUNS.md`).

| Pack | Tax | Statutory overtime (weekly part only) | Notes |
|---|---|---|---|
| CA-NB | yes | after 44 h, 1.5 x minimum wage | |
| CA-BC | yes, with BC tax reduction | after 40 h, 1.5 x wage | daily (8 h) and double time not modelled |
| CA-AB | yes | after 44 h, 1.5 x wage | daily 8 h rule not modelled |
| CA-SK | yes | after 40 h, 1.5 x wage | daily rule not modelled |
| CA-MB | yes, BPA phase-out (net income approximated by taxable income) | after 40 h, 1.5 x wage | daily rule not modelled |
| CA-ON | yes, surtax, health premium, tax reduction | after 44 h, 1.5 x wage | |
| CA-NS | yes | after 48 h, 1.5 x wage | managers etc. at minimum wage not modelled |
| CA-PE | yes | after 48 h, 1.5 x wage | top 20% bracket over 200,000 is listed as proposed (Bill 23), applied for all of 2026; low-income reduction not modelled |
| CA-NL | yes | none | overtime is paid at a minimum overtime rate ($24.53 from 2026-04-01) and the multiplier rule was not confirmed; left out |
| CA-YT | yes (federal-style BPA) | none | no official source retrieved |
| CA-NT | yes | after 40 h, 1.5 x wage | daily rule not modelled |
| CA-NU | yes | after 40 h, 1.5 x wage | daily rule not modelled |

Not yet: Quebec (own system: QPP, QPIP, provincial return).

## United States

| Pack | Modelled | Overtime | Not modelled |
|---|---|---|---|
| US-2026 | Federal income tax (single, married filing jointly or head of household, chosen in the app; standard deduction 16,100 / 32,200 / 24,150; brackets 10-37%; head-of-household brackets are from Tax Foundation citing Rev. Proc. 2025-32, to be confirmed), Social Security (6.2% to 184,500), Medicare 1.45%, Additional Medicare 0.9% over 200,000 | after 40 h, 1.5 x wage (FLSA) | married filing separately, spouse income, credits, itemizing, the 2025-2028 overtime/tips deductions, all state and local tax, state unemployment benefits, state overtime rules |

Sources: IRS inflation adjustments for 2026, IRS Topic 751, DOL Fact Sheet 23. Tests are `derived`
from `tools/reference_us.py`. 
State packs (all extend `US-2026`, tier `partial`, tests derived from `tools/reference_us_states.py`):

| Pack | Tax | Source |
|---|---|---|
| US-AK, FL, NV, NH, SD, TN, TX, WA, WY | none on wages | Tax Foundation 2026 (third party: confirm against each state when convenient). WA payroll premiums not modelled |
| US-PA | 3.07% flat, no deduction | PA Department of Revenue (official); local earned-income taxes not modelled |
| US-IL | 4.95% flat after one 2,925 exemption | Illinois Comptroller Payroll Bulletin 1-26 (official); high-income exemption phase-out not modelled |
| US-MI | 4.25% flat after one 5,900 personal exemption | Michigan Treasury, calendar-year withholding page (official); city taxes not modelled |
| US-KY | 3.5% flat after the 3,360 standard deduction | Kentucky DOR 2026 withholding formula (official); local occupational taxes not modelled |
| US-GA | 4.99% flat after the 15,000 single standard deduction | Georgia DOR 2026 employer's tax guide, June 2026 revision (official) |
| US-CA | FTB 2026 Schedule X (single) after the 5,900 standard deduction and 158 exemption credit, plus 1.3% SDI on all wages | FTB Tax News Oct 2026 and EDD (official). Complete 2026 schedules are due in late December: re-check then. Mental Health Services Tax over 1M, other filing statuses, renter's credit and daily overtime not modelled |

Held back for lack of an official source for the full mechanics: IN (2.95% rate confirmed on in.gov, exemption and county taxes not), NC, MS, UT, CO, AZ and the other flat-tax states. Graduated states (CA, NY, ...) are not started.
