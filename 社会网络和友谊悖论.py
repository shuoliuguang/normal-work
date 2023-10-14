import numpy as np
import pandas as pd
import random
from texttable import Texttable

def initial_not_random(n, r):
    global net
    net = np.zeros([n, n])
    for i in range(n):
        for j in range(r):
            jj = (i+j+1) % n
            net[i][jj] = net[jj][i] = 1

def initial_random(n, r):
    global net
    net = np.zeros([n, n])
    max_trial = n
    for i in range(n):
        trial = 0
        while np.sum(net[i] == 1) < r:
            trial += 1
            temp = np.sum(net[i] == 1)
            j = random.randint(0, n - 1)
            if j is not i and np.sum(net[j] == 1) < r:
                net[i][j] = net[j][i] = 1
            if (trial > max_trial):
                break

def adjust(num):
    global net
    for i in range(num):
        edges = np.nonzero(net)
        empty = np.nonzero(net == 0)
        ran1 = random.randint(0, len(edges[0])-1)
        ran2 = random.randint(0, len(empty[0])-1)
        net[edges[0][ran1]][edges[1][ran1]] = net[edges[1][ran1]][edges[0][ran1]] = 0
        net[empty[0][ran2]][empty[1][ran2]] = net[empty[1][ran2]][empty[0][ran2]] = 1

def count_degree(n):
    global net
    cnt = []
    cnt = [np.sum(net[i] == 1) for i in range(n)]
    return cnt

def compare_degree(n, cnt):
    global net
    comp = []
    for i in range(n):
        neighbors = np.nonzero(net[i])
        if len(neighbors[0]):
            mean = np.mean(np.array(cnt)[neighbors[0]])
        else:
            mean = 0
        comp.append(mean)
    return comp

stats=[0]*11
a=[1]*10
j=0
while(j<2):
  if(j==0):
      stats[0]='网络个数'
      j=1
  else:
      N = 100
      while (N > 0):
          N += 1
          n = random.randrange(50, 1000, 2)
          r = random.randint(4, 10)
          p = random.uniform(0, 1)
          initial_random(n, r)
          adjust(N)
          cnt = count_degree(n)
          comp = compare_degree(n, cnt)
      if (comp >= 0 and comp < 0.1 and a[0]==1):
          stats[1]=cnt
          a[0]=0
      if (comp >= 0.1 and comp < 0.2 and a[1]==1):
          stats[2]=cnt
          a[1]=0
      if (comp >= 0.2and comp < 0.3 and a[2]==1):
          stats[3]=cnt
          a[2]=0
      if (comp >= 0.3 and comp < 0.4 and a[3]==1):
          stats[4]=cnt
          a[3] = 0
      if (comp >= 0.4 and comp < 0.5 and a[4]==1):
          stats[5]=cnt
          a[4] = 0
      if (comp >= 0.5 and comp < 0.6 and a[5]==1):
          stats[6]=cnt
          a[5] = 0
      if (comp >= 0.6 and comp < 0.7 and a[6]==1):
          stats[7]=cnt
          a[6] = 0
      if (comp >= 0.7 and comp < 0.8 and a[7]==1):
          stats[8]=cnt
          a[7] = 0
      if (comp >= 0.8 and comp < 0.9 and a[8]==1):
          stats[9]=cnt
          a[8] = 0
      if (comp >= 0.9 and comp <=1.0 and a[9]==1):
          stats[10]=cnt
          j=2

columns = ['占比', '[0，0.1)', '[0.1，0.2)','[0.2，0.3)','[0.3，0.4)','[0.4，0.5)','[0.5，0.6)','[0.6，0.7)','[0.7，0.8)','[0.8，0.9)','[0.9，1.0]']
df = pd.DataFrame(data=stats, columns=columns)
print('stats内容')
print(df)

print('stats内容')
tb = Texttable()  
tb.set_cols_align(['l', 'r', 'r'])  
tb.set_cols_dtype(['i', 'i', 'i'])  
tb.header(df.columns)  
tb.add_rows(df.values, header=False)  
print(tb.draw()) 