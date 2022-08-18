'字符串相关'

UNITS = 'KMGTPEZYBND'

def strsize(x):
    unit = 'B'
    for du in UNITS:
        if x < 10:
            return '%.2f %s' % (x,unit)
        if x < 1000:
            return '%.1f %s' % (x,unit)
        unit = du + 'B'
        x /= 1024.0
    return '%g %s' % (x,unit)

year_len = 365.2422 #一年的天数
mon_len = year_len / 12

def strtime(a):
    a *= 1e15
    us = ['fs','ps','ns','us','ms','s','min','h', 'days','months','years','centuries']
    ks = [1000,1000,1000,1000,1000, 60,   60, 24,mon_len,      12,    100,]
    n = len(ks)
    for i in range(n):
        if a < ks[i]:
            du = us[i]
            break
        a /= ks[i]
    else:
        du = us[n]
    return '%.8g %s' % (a,du)

def _test():
    xs = (0,1,100,10**7,123<<30,907<<30,1008<<30,234<<180)
    for x in xs:
        print(strsize(x))
    for x in xs:
        print(strtime(x))

if __name__=='__main__':
    _test()
