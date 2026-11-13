from decimal import Decimal as D, ROUND_HALF_UP
BS=[(12400,.10),(50400,.12),(105700,.22),(201775,.24),(256225,.32),(640600,.35),(10**12,.37)]
BM=[(24800,.10),(100800,.12),(211400,.22),(403550,.24),(512450,.32),(768700,.35),(10**12,.37)]
BH=[(17700,.10),(67450,.12),(105700,.22),(201750,.24),(256200,.32),(640600,.35),(10**12,.37)]
SD={1:(BS,16100),2:(BM,32200),3:(BH,24150)}
def tax(g,fs=1):
    B,sd=SD[fs]
    ti=max(D(0),D(g)-sd); t=D(0); lo=D(0)
    for hi,r in B:
        hi=D(hi)
        if ti>lo: t+=(min(ti,hi)-lo)*D(str(r))
        lo=hi
    return t
q=lambda x:x.quantize(D('0.001'),ROUND_HALF_UP)
print("# US")
NAMES={1:"single",2:"mfj",3:"hoh"}
for fs in (1,2,3):
  for g in (12000,30000,60000,150000,300000,700000,900000):
    g=D(g); ss=min(g,D(184500))*D('0.062'); me=g*D('0.0145'); ad=max(D(0),g-200000)*D('0.009')
    print(f"  - id: us-{NAMES[fs]}-{int(g)}\n    status: derived\n    inputs: {{ gross_annual: {int(g)}, filing_status: {fs}, as_of: 2026-11-12 }}\n    expect: {{ fed.tax: {q(tax(g,fs))}, ss.tax: {q(ss)}, medicare.tax: {q(me)}, medicare.additional: {q(ad)}, \"@contributions\": {q(ss+me+ad)} }}")
