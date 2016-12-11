import numpy as np
import math


def ReadFile():
    grid = []
    noisy_dist = []
    with open("./hmm-data.txt", "r") as fo:
        for i, line in enumerate(fo):
            if i >= 2 and i < 12:
                line_N = line.split()
                grid.append(line_N)

            if i >= 24 and i < 35:
                line_N = line.split()
                noisy_dist.append(line_N)

    grid = [[int(y) for y in x] for x in grid]
    grid = np.array(grid)
    noisy_dist = [[float(y) for y in x] for x in noisy_dist]
    noisy_dist = np.array(noisy_dist)
    return grid, noisy_dist


def Distance(t1, t2, Rx, Ry):
    x = t1
    y = t2
    d = math.sqrt(abs(Rx - x) ** 2 + abs(Ry - y) ** 2)
    return d


def HMM(grid, nd):
    n = np.count_nonzero(grid == 1)
    prior = np.zeros((n, 1))
    for i in range(n):
        prior[i][0] = 1 / float(n)
    X = np.zeros((n, n))
    Z = np.zeros((10, 10))
    Z = Z.astype(int)
    p = 1
    for i in range(10):
        for j in range(10):

            if (grid[i][j] != 0):
                Z[i][j] = p
                p = p + 1
    for i in range(10):
        for j in range(10):
            count = 0
            if (Z[i][j] != 0):
                if (j != 9 and Z[i][j + 1] != 0):
                    count = count + 1
                if (i != 9 and Z[i + 1][j] != 0):
                    count = count + 1
                if (j != 0 and Z[i][j - 1] != 0):
                    count = count + 1
                if (i != 0 and Z[i - 1][j] != 0):
                    count = count + 1
            if (Z[i][j] != 0):
                k = Z[i][j]
                if (j != 9 and Z[i][j + 1] != 0):
                    m = Z[i][j + 1]
                    X[m - 1][k - 1] = 1 / float(count)
                if (i != 9 and Z[i + 1][j] != 0):
                    m = Z[i + 1][j]
                    X[m - 1][k - 1] = 1 / float(count)
                if (j != 0 and Z[i][j - 1] != 0):
                    m = Z[i][j - 1]
                    X[m - 1][k - 1] = 1 / float(count)
                if (i != 0 and Z[i - 1][j] != 0):
                    m = Z[i-1][j]
                    X[m - 1][k - 1] = 1 / float(count)

    diagonal = 9 * math.sqrt(2)
    D1 = np.zeros(int(diagonal * 10))
    k = 0.0
    for i in range(int(diagonal * 10)):
        D1[i] = k
        k = k + 0.1

    E1 = Evidence(Z, D1, 0, 0, n)
    E1[0][0] = 1
    E2 = Evidence(Z, D1, 0, 9, n)
    E2[0][9] = 1.0
    E3 = Evidence(Z, D1, 9, 0, n)
    E3[0][77] = 1.0
    E4 = Evidence(Z, D1, 9, 9, n)
    E4[0][86] = 1.0
    probableloc=[]
    for i in range(len(nd)):
        for j in range(int(diagonal * 10)):
            if (np.isclose(nd[i][0], D1[j])):
                er1 = j
        for j in range(len(D1)):
            if (np.isclose(nd[i][1], D1[j])):
                er2 = j
        for j in range(len(D1)):
            if (np.isclose(nd[i][2], D1[j])):
                er3 = j
        for j in range(len(D1)):
            if (np.isclose(nd[i][3], D1[j])):
                er4 = j
        l1 = FindLoc(E1, er1)
        l2 = FindLoc(E2, er2)
        l3 = FindLoc(E3, er3)
        l4 = FindLoc(E4, er4)
        c, c1, c2 = [], [], []
        c1 = list(set(l1).intersection(l2))
        c2 = list(set(l3).intersection(l4))
        c = list(set(c1).intersection(c2))
        c.sort()
        probableloc.append(c)
    return probableloc,X,Z

def FindLoc(E, er):
    l = []
    for s in range(len(E[er])):
        if E[er][s] != 0:
            l.append(s)
    return l

def Evidence(Z, D1, t1, t2, n):
    diagonal = 9 * math.sqrt(2)
    E = np.zeros((int(diagonal * 13), n))
    for i in range(10):
        for j in range(10):
            d = round(Distance(t1, t2, i, j), 1)
            lb = round(d * 0.7, 1)
            ub = round(d * 1.3, 1)
            a = np.arange(lb, ub, 0.1)
            list_count = len(a)
            m = Z[i][j]
            for ind in range(int(diagonal * 10)):
                if (np.isclose(lb, D1[ind])):
                    loc = ind
                    break
            for k in range(list_count):
                E[loc + k][m - 1] = 1 / float(list_count)


    return E



def findNeighbours(location,X):
    a=[]
    for i in range(87):
        if(X[i][location-1]!=0):
            a.append(i+1)
    return a

count =0
def Path(p,X,location_list,i,Z):
    global count, fin_path
    a = findNeighbours(p, X)
    fin_path.append(p)
    if(count==10):
        print "-----------------------------\n The robot's path is as follows :\n"
        Coord(fin_path,Z)
        exit()
        
    elif (len(a) != 0):
        for k in a:
            if k in location_list[i + 1]:
                count = count +1
                Path(k, X, location_list, i+1,Z)


def Coord(fin_path,Z):
    for k in range(len(fin_path)):
        for i in range(10):
            for j in range(10):
                if(Z[i][j]==fin_path[k]):
                    print "Timestamp -X {}".format(k+1),
                    if(k!=10):
                        print "(",i,",",j,") -->"
                    else:
                        print "(",i,",",j,")"
    
    
            

grid, nd = ReadFile()
location_list,X,Z=HMM(grid, nd)
fin_path=[]
for i in range(len(location_list[0])):
    count =0
    fin_path=[]
    Path(location_list[0][i],X, location_list,0,Z)
