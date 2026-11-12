from decimal import Decimal as D, ROUND_HALF_UP
B=[(12400,.10),(50400,.12),(105700,.22),(201775,.24),(256225,.32),(640600,.35),(10**12,.37)]
def tax(g):
    ti=max(D(0),D(g)-16100); t=D(0); lo=D(0)
    for hi,r in B:
        hi=D(hi)
        if ti>lo: t+=(min(ti,hi)-lo)*D(str(r))
        lo=hi
    return t
q=lambda x:x.quantize(D('0.001'),ROUND_HALF_UP)
print("# US")
for g in (12000,16100,30000,60000,105700+16100,150000,300000,700000):
    g=D(g); ss=min(g,D(184500))*D('0.062'); me=g*D('0.0145'); ad=max(D(0),g-200000)*D('0.009')
    print(f"  - id: us-{int(g)}\n    status: derived\n    inputs: {{ gross_annual: {int(g)}, as_of: 2026-11-12 }}\n    expect: {{ fed.tax: {q(tax(g))}, ss.tax: {q(ss)}, medicare.tax: {q(me)}, medicare.additional: {q(ad)}, \"@contributions\": {q(ss+me+ad)} }}")
