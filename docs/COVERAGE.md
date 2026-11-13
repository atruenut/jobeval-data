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

| CA-QC | **estimate** | none (CNESST rule not checked) | Quebec brackets and BPA, QPP (6.3%, second ceiling), QPIP 0.43%, reduced EI 1.30%, 16.5% federal abatement. Revenu Quebec's own payroll formulas could not be retrieved, so the deduction for workers (max 1,450) and the credit/deduction treatment of QPP, EI and QPIP premiums are not applied: Quebec tax is overstated by a few hundred dollars a year. Promote to partial once TP-1015.F-V is read |

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
| US-AZ | 2.5% flat after the standard deduction (8,350 single, 16,700 joint) | Tax Foundation 2026 (third party); HoH uses the single amount; dependent credit not modelled |
| US-CO | 4.4% flat of federal taxable income | Tax Foundation 2026 (third party); rate can change under TABOR refund rules |
| US-IN | 2.95% flat after the personal exemption (1,000 single, 2,000 joint) | Tax Foundation 2026 (third party); county income taxes not modelled; drops to 2.9% in 2027 |
| US-LA | 3% flat after the standard deduction (12,875 single, 25,750 joint) | Tax Foundation 2026 (third party); HoH uses the single amount |
| US-NC | 3.99% flat after the 12,750 single standard deduction | NC DOR NC-30 for 2026 (official) |

Bracketed state packs (tier `partial`, or `estimate` where a large item is not modelled), generated by `tools/gen_us_graduated.py` from `tools/us_graduated_data.py`; source for all: Tax Foundation, 2026 State Individual Income Tax Rates and Brackets (third party). Tax is the state bracket schedule applied to income less the state standard deduction and personal exemption (or federal taxable income for states that start from it: DC, ID, IA, MO, MT, NM, ND), less simple credits. Married filing jointly uses the joint thresholds and amounts; head of household uses the single ones. Local taxes, phase-outs and most credits are not modelled and are listed in each pack's `not_modelled`.

| Packs | Notes |
|---|---|
| US-AL, AR, DE, DC, HI, ID, IA, KS, ME, MD, MA, MN, MS, MO, MT, NE, NJ, NM, NY, ND, OH, OK, RI, SC, VT, VA, WV, WI | partial |
| US-AL, CT, OR, UT | estimate: Alabama's federal-tax deduction, Connecticut's exemption phase-out and recapture, Oregon's federal-tax subtraction and Utah's credit phase-out are missing, so these overstate tax |

All 50 states and DC now have a pack. Re-check the third-party figures against each state's revenue department when convenient.

## United Kingdom

| Pack | Modelled | Overtime | Not modelled |
|---|---|---|---|
| GB-2026 (tax year 6 Apr 2026 to 5 Apr 2027) | Income tax for England, Wales and Northern Ireland (Personal Allowance 12,570 with the 100,000 taper; 20/40/45%), employee Class 1 National Insurance (8% between 12,570 and 50,270, 2% above) | none (the UK has no statutory overtime pay) | student loan, pension deductions, savings/dividend/marriage allowances, tax codes, benefits in kind, unemployment benefit |
| GB-SCT-2026 | Scottish bands (19/20/21/42/45/48%) replacing the rest-of-UK income tax; same NI | none | as above; the Scottish Government page called the 2026-27 bands "proposed": confirm against the final Budget order |

Sources: GOV.UK income tax rates, GOV.UK NI rates and allowances (monthly thresholds 1,048 and 4,189
match the annual 12,570 and 50,270), Scottish Government rates and bands. Tests are `derived` from
`tools/reference_gb.py`. Wales and Northern Ireland use the rest-of-UK rates (Wales sets no different rates today).

## New Zealand and Australia

| Pack | Modelled | Source | Not modelled |
|---|---|---|---|
| NZ-2026 (1 Apr 2026 to 31 Mar 2027, partial) | Resident income tax (10.5/17.5/30/33/39%), ACC earners' levy 1.75% to a 156,641 cap | Deloitte New Zealand highlights 2026 and Baker Tilly Staples Rodway 2026 Tax Facts (third party; confirm against IRD) | KiwiSaver (optional), student loan, Working for Families, jobseeker support. No statutory overtime |
| AU-2026 (1 Jul 2026 to 30 Jun 2027, estimate) | Resident income tax with the 16% band cut to 15%, Low Income Tax Offset, Medicare levy | Super Guide (third party; the ATO site was not reachable) | The 2026-27 Medicare thresholds were not announced, so 2025-26 ones are used; Medicare surcharge, HECS-HELP, deductions, proposed 2026-27 Budget measures. Overtime is set by awards, so none |

## Ireland

| Pack | Modelled | Source | Not modelled |
|---|---|---|---|
| IE-2026 (calendar 2026, partial) | Income tax 20/40% to a 44,000 cut-off less the 2,000 personal and 2,000 employee credits (single person), USC (0.5/2/3/8%), employee PRSI (4.20% to 30 Sep, 4.35% from 1 Oct: modelled as a 4.2375% whole-year blend, with the 352 a week exemption and the tapered 12 a week credit) | gov.ie PRSI page (official); Grant Thornton and BrightPay for tax and USC (third party; the 2% USC band top, 28,700, comes from two sources, one other said 27,800) | Reliefs, pension, married/one-parent credits, medical-card USC rate, jobseeker's benefit. No statutory overtime |

## Germany

| Pack | Modelled | Source | Not modelled |
|---|---|---|---|
| DE-2026 (calendar 2026, partial) | Tax class I income tax by the statutory section 32a tariff (basic allowance 12,348), solidarity surcharge (20,350 allowance, 11.9% cap), employee pension, unemployment, health (7.3% plus half the 2.9% average extra) and care (1.8%, +0.6% if childless) with the 2026 ceilings; a children choice input | § 32a EStG (official); AOK, TK and WunderTax for the rest (third party) | Church tax, other tax classes and splitting, exact Vorsorgepauschale, private health insurance, child allowances, whole-euro rounding. No statutory overtime premium |
