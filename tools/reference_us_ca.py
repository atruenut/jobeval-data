#!/usr/bin/env python3
"""Reference for US-CA-2026 from the FTB 2026 Schedule X table (base amount + rate x excess), single filer.
Own arithmetic, not an official run.  python3 tools/reference_us_ca.py"""
from decimal import Decimal as D, ROUND_HALF_UP
X=[(0, 0, '0.01'), (11456, '114.56', '0.02'), (27157, '428.58', '0.04'), (42861, '1056.74', '0.06'), (59498, '2054.96', '0.08'), (75197, '3310.88', '0.093'), (384109, '32039.70', '0.103'), (460927, '39951.95', '0.113'), (768213, '74675.27', '0.123')]
def tax(g):
    ti=max(D(0),D(g)-5900)
    for lo,base,r in reversed(X):
        if ti>=lo: t=D(base)+(ti-lo)*D(r); break
    return max(D(0),t-158)
q=lambda x:x.quantize(D("0.001"),ROUND_HALF_UP)
if __name__=="__main__":
    for g in (5000,30000,80000,150000,500000,900000):
        print(g, q(tax(g)), q(D(g)*D("0.013")))
