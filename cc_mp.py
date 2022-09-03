'matplotlib 相关'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import font_manager

plt.rcParams['xtick.direction'] = 'in' #将tick放入内内侧
plt.rcParams['ytick.direction'] = 'in'

def setup_paper_figure():
    '论文绘图样式'
    plt.rc('font',family='Times New Roman')
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Times New Roman'
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
    plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

mp_colors=['r','g','b','m','c','y',
        'orange','lime','forestgreen','slategrey','royalblue',
        'pink','magenta','blueviolet',
        'coral','olive','cadetblue','lightskyblue','darkseagreen',
        'navy','thistle','darkcyan',]

mp_linestyles = ['-','--',':','-.']
mp_markers_filled = {'o','v','^','<','>'}
mp_markers = ['o','v','^','<','>','x','+']

def get_session_value(session:dict,values:list,key):
    '返回 key 对应的唯一值'
    try:
        return session[key]
    except KeyError:
        pass
    i = len(session)
    i %= len(values)
    ans = values[i]
    session[key] = ans
    return ans

GLB_SESSION = {}

def get_session_color(key,session=GLB_SESSION)->str:
    return get_session_value(session.setdefault('color',{}),mp_colors,key)

def get_session_linestyle(key,session=GLB_SESSION)->str:
    return get_session_value(session.setdefault('linestyle',{}),mp_linestyles,key)

def get_session_marker(key,session=GLB_SESSION)->str:
    return get_session_value(session.setdefault('marker',{}),mp_markers,key)

def plot_fin(show=True,tight=True):
    plt.grid(True,which='major',linestyle=':',color='gray')
    plt.grid(True,which='minor',linestyle=':',color=(0.7,0.7,0.7))
    if tight:plt.tight_layout()
    if show:plt.show()

def plot(*a,
    xlabel=None,ylabel=None,label=None,
    color=None,linestyle=None,marker=None,
    color_key=None,linestyle_key=None,marker_key=None,
    **k):
    color_key = color_key or label
    color = color or get_session_color(color_key)
    if linestyle is None:
        if linestyle_key is not None:
            linestyle = get_session_linestyle(linestyle_key)
        else:
            linestyle = '-'
    if marker is None:
        if marker_key is not None:
            marker = get_session_marker(marker_key)
        else:
            marker = 'o'
    if marker == 'none':
        marker = None
    ka = dict(linestyle=linestyle,marker=marker,color=color,label=label)
    if marker in mp_markers_filled:
        ka['markerfacecolor'] = 'none'
    k.update(ka)
    plt.plot(*a,**k)
    if xlabel:plt.xlabel(xlabel)
    if ylabel:plt.ylabel(ylabel)

def _test():
    x = np.linspace(-5,5,100)
    for func in ('sin','cos'):
        f = getattr(np,func)
        y = f(x)
        plot(x,y,label=func,xlabel='x',ylabel='y')
    plt.legend()
    plot_fin()

if __name__ == '__main__':
    _test()
