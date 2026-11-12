#!/usr/bin/env python3
"""Independent reference for CA-NB-2026 take-home figures, written directly from CRA T4127
(122nd ed., 2026) wording and NOT from the pack YAML, so golden `derived` tests catch
wiring mistakes in the pack. It is still our own arithmetic: it is not an official run.

    python3 tools/reference_ca_nb.py 50000 80000
"""
import sys
from decimal import Decimal as D, ROUND_HALF_UP

CPP_RATE, CPP_BASE, CPP_ENH = D("0.0595"), D("0.0495"), D("0.01")
EXEMPT, YMPE, YAMPE, CPP2 = D(3500), D(74600), D(85000), D("0.04")
EI_RATE, EI_MAX = D("0.0163"), D(68900)
CEA = D(1501)
FED = [(D(58523), D("0.14")), (D(117045), D("0.205")), (D(181440), D("0.26")), (D(258482), D("0.29")), (None, D("0.33"))]
NB = [(D(52333), D("0.094")), (D(104666), D("0.14")), (D(193861), D("0.16")), (None, D("0.195"))]
FED_BPA_MAX, FED_BPA_MIN, PHASE_LO, PHASE_HI = D(16452), D(14829), D(181440), D(258482)
NB_BPA = D(13664)


def bracket_tax(x, table):
    tax, lo = D(0), D(0)
    for top, rate in table:
        hi = x if top is None else min(x, top)
        if hi > lo:
            tax += (hi - lo) * rate
        if top is None or x <= top:
            break
        lo = top
    return tax


def calc(gross, other=0):
    g = D(gross)
    o = D(other)
    c = max(D(0), min(g, YMPE) - EXEMPT) * CPP_RATE
    c2 = max(D(0), min(g, YAMPE) - YMPE) * CPP2
    ei = min(g, EI_MAX) * EI_RATE
    enhanced = c * CPP_ENH / CPP_RATE + c2
    base_credit = c * CPP_BASE / CPP_RATE
    a = g + o - enhanced
    bpa = FED_BPA_MAX if a <= PHASE_LO else FED_BPA_MIN if a >= PHASE_HI else \
        FED_BPA_MAX - (FED_BPA_MAX - FED_BPA_MIN) * (a - PHASE_LO) / (PHASE_HI - PHASE_LO)
    fed = max(D(0), bracket_tax(a, FED) - D("0.14") * (bpa + base_credit + ei + min(g, CEA)))
    nb = max(D(0), bracket_tax(a, NB) - D("0.094") * (NB_BPA + base_credit + ei))
    ei_weekly = lambda prior: min(D("0.55") * min(D(prior), EI_MAX) / 52, D(729))
    return dict(cpp_base_credit=base_credit, cpp_base=c, cpp_second=c2, ei=ei, enhanced=enhanced, taxable=a, bpa=bpa, fed=fed, nb=nb)


if __name__ == "__main__":
    for g in sys.argv[1:]:
        r = calc(g)
        print(g, {k: str(v.quantize(D("0.001"), ROUND_HALF_UP)) for k, v in r.items()})
