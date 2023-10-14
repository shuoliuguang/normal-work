# -*- coding: utf-8 -*-
"""

@author: minus
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar




class PriceFunc(object):
    def __init__(self, name, function, num):
        self.name = name
        self.function = function
        self.num = num

    def __str__(self):
        return self.name


def stable(p0, z1, z2, rnd): 
    return 0.5


def scaled(p0, z1, z2, rnd): 
  
    if z1 == None:
        return 0.5
    elif z1 < z2:
        return 1.2 * p0
    elif z1 > z2:
        return 0.8 * p0
    else:
        return p0


def venal(p0, z1, z2, rnd):  
    k = 1 + 4 * z2 * z2
  
    return 0.1 + k / 2


def stable_high(p0, z1, z2, rnd):
    return 0.9
   

def patient(p0, z1, z2, rnd):
    if z1 == None:
        return 0.9
    elif z2 > z1 and p0 == 0.9:
        return 0.9  
    elif z2 == z1 and p0 == 0.9:
 
        W = lambda p: -1 * (p - 0.2) * (1 - p / (1 + 4 * (1 - p / (1 + 4 * z2 * z2)) ** 2))
        res = minimize_scalar(W, bounds=(0, 5), method='bounded')
        return (res.x + p0) / 2
       
    else:
        W = lambda p: -1 * (p - 0.2) * (1 - p / (1 + 4 * (1 - p / (1 + 4 * z2 * z2)) ** 2))
        res = minimize_scalar(W, bounds=(0, 5), method='bounded')
        return res.x


def best(p0, z1, z2, rnd):
    if rnd == 1:
        return 0.325
    elif rnd == 100:
        return venal(p0, z1, z2, rnd)
    else:
        return 0.918


def profit_monthly(priceFunc):
    profit_sum = 0
    n = 0
    p = None
    z1 = None
    z2 = 0
    z_list = []
    p_list = []
    profit_mon_list = []
    profit_sum_list = []
    while True:
        n += 1
        p = priceFunc.function(p, z1, z2, n) 
        p_list.append(p)
        z = 1 - p / (1 + 4 * z2 * z2)  
        z_list.append(z)
        profit_mon = (p - 0.2) * z
        profit_mon_list.append(profit_mon)
        profit_sum += profit_mon
        profit_sum_list.append(profit_sum)
        z1 = z2  
        z2 = z 
        if n % 10 == 0:  
            f.write('%.3f,' % profit_sum)
            print('%.3f' % profit_sum, end='\t')
        if n == 100:
            break
    f.write('\n')
    print()

    fig, (ax1, ax3) = plt.subplots(1, 2)
    fig.suptitle(priceFunc.name)
    ax1.set_title('profit')
    ax3.set_title('scale')
    
    color1 = 'tab:red'
    color2 = 'tab:blue'
    xPoints = np.array(list(range(1, 101)))
    yPoints = np.array(profit_mon_list)
    ax1.plot(xPoints, yPoints, color=color1)
    ax1.set_xlabel('month')
    ax1.set_ylabel('profit mon', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    ax2.set_ylabel('profit sum', color=color2)
    yPoints2 = np.array(profit_sum_list)
    ax2.plot(xPoints, yPoints2, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    yPoints3 = np.array(z_list)
    ax3.plot(xPoints, yPoints3, color=color1)
    ax3.set_xlabel('month')
    ax3.set_ylabel('scale', color=color1)
    ax3.tick_params(axis='y', labelcolor=color1)
    ax4 = ax3.twinx()
    ax4.set_ylabel('price', color=color2)
    yPoints4 = np.array(p_list)
    ax4.plot(xPoints, yPoints4, color=color2)
    ax4.tick_params(axis='y', labelcolor=color2)
    fig.set_size_inches(6, 3)
    fig.tight_layout()
    fig.savefig('./%i_%s.png' % (priceFunc.num, priceFunc.name), dpi=300)


f = open('./profit.csv', 'w', encoding='utf-8-sig')
f.write('模拟进行月数,')
print('模拟进行月数', end='\t')
for i in range(10, 101, 10):
    f.write('%i,' % i)
    print('%i' % i, end='\t')
f.write('\n')
print()


funcList = [stable, scaled, venal, patient, stable_high, best]
titles = ['stable pricing', 'scaled pricing', 'venal pricing', 'patient pricing', 'stable high', 'best pricing']

for i in range(len(funcList)):
    priceFunc = PriceFunc(titles[i], funcList[i], i + 1)
    f.write('%s,' % titles[i])
    print('%s' % titles[i], end='\t')
    profit_monthly(priceFunc)

f.close()
