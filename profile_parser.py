import re
import pandas as pd

datas = []
begin = False
with open('export_profile.txt', 'r', encoding='gbk') as f:
    for ln in f:
        s = re.split(r'\s+', ln)
        s = filter(None, s)
        s = list(s)
        if not s:continue
        if s[0] == 'ncalls':
            begin = True
            s.extend(s.pop().split(':'))
            columns = s
            continue
        if not begin:continue
        if len(s) > 5:
            s = s[:5] + [' '.join(s[5:])]
        try:
            n1, n2 = s[0].split('/')
        except Exception:
            n = int(s[0])
        else:
            n = min(map(int, (n1, n2)))
        try:
            s.extend(s.pop().split(':'))
            s1 = list(map(float, s[1:5]))
            da = [n, *s1, *(s[5:])]
        except Exception:
            continue
        datas.append(da)
df = pd.DataFrame(datas, columns=columns)
df.to_excel('export_profile.xlsx', index=False)
