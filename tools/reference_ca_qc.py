#!/usr/bin/env python3
"""Reference for CA-QC-2026 (own arithmetic, not an official run). Federal side in the CRA payroll
form R x A - K (T4032QC Chart 1, with K recomputed exactly by continuity; the printed K is
asserted to be within 0.5), 16.5% abatement, QPP/EI/QPIP per Revenu Quebec and CRA. Provincial
side: Quebec brackets less 14% of the basic personal amount, as the pack documents.
    python3 tools/reference_ca_qc.py [--tests]"""
import sys
from decimal import Decimal as D, ROUND_HALF_UP

FED = [(0, D("0.14"), 0), (58523, D("0.205"), 3804), (117045, D("0.26"), 10241), (181440, D("0.29"), 15685), (258482, D("0.33"), 26024)]
def exact_k():
    ks = [D(0)]
    for i in range(1, len(FED)):
        ks.append(ks[-1] + FED[i][0] * (FED[i][1] - FED[i - 1][1]))
    for (a, r, printed), k in zip(FED, ks):
        assert abs(k - printed) < D("0.5"), (a, k, printed)
    return ks
KS = exact_k()
QB = [(54345, D("0.14")), (108680, D("0.19")), (132245, D("0.24")), (None, D("0.2575"))]

def qpp(g):
    g = D(g)
    base = max(D(0), min(g, D(74600)) - 3500) * D("0.063")
    second = max(D(0), min(g, D(85000)) - 74600) * D("0.04")
    return base, second

def calc(g):
    g = D(g)
    base, second = qpp(g)
    ei = min(g, D(68900)) * D("0.013")
    qpip = min(g, D(103000)) * D("0.0043")
    deduction = base * D("0.01") / D("0.063") + second
    ti = g - deduction
    idx = max(i for i, (a, _, _) in enumerate(FED) if ti >= a)
    basic = FED[idx][1] * ti - KS[idx]
    credits = D("0.14") * (D(16452) + base * D("0.053") / D("0.063") + ei + qpip + min(g, D(1501)))
    fed = max(D(0), basic - credits) * D("0.835")
    qt = D(0); lo = D(0)
    for hi, r in QB:
        top = ti if hi is None else min(ti, D(hi))
        if top > lo: qt += (top - lo) * r
        if hi is not None: lo = D(hi)
    qc = max(D(0), qt - D("0.14") * D(18952))
    return dict(fed=fed, qc=qc, qpp=base, qpp2=second, ei=ei, qpip=qpip)

q = lambda x: x.quantize(D("0.001"), ROUND_HALF_UP)
if __name__ == "__main__":
    for g in (20000, 45000, 70000, 80000, 120000):
        r = calc(g)
        print(f"  - id: qc-{g}\n    status: derived\n    inputs: {{ gross_annual: {g}, as_of: 2026-11-12 }}\n    expect: {{ fed.tax: {q(r['fed'])}, qc.tax: {q(r['qc'])}, cpp.base: {q(r['qpp'])}, cpp.second: {q(r['qpp2'])}, ei.premium: {q(r['ei'])}, qpip.premium: {q(r['qpip'])} }}")
