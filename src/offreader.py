import math

def sqlength(edge):
    global el
    global d
    a = 0
    
    v1 = min(edge)
    v2 = max(edge)
    for i in range(d):
        a += (el[0][v1][i] - el[0][v2][i])**2

    return a

off = open("input.off", "r")

count = [] # element counts
edges = set([])
d = 0 # rank of polytope

cur = 0 # current element rank

lines = off.readlines()

# parse element data
i = -1
while i < len(lines)-1:
    i += 1
    line = lines[i]

    if("OFF" in line):
        continue
    if(line[0] == '#'):
        continue
    if(line == '\n'):
        continue

    if(cur != 1):
        l = list(map(int,line.rstrip().split(' ')))

    if(cur == 0): # parse element counts
        count = l
        d = len(count)

        a = count[1]
        count[1] = count[2]
        count[2] = a

        el = [[] for j in range(d)]

        cur += 1
        continue
    
    if(cur == 1): # vertices
        l = list(map(float,line.rstrip().split(' ')))
        for j in range(count[0]):
            el[0].append(l)

            i += 1
            line = lines[i]
            if(j+1 == count[0]):
                break
            l = list(map(float,line.rstrip().split(' ')))
        cur += 1
        continue

    if(cur == 2): # faces
        for j in range(count[2]):
            for k in range(1, l[0]):
                edges.add(frozenset([l[k],l[k+1]]))
            edges.add(frozenset([l[1],l[-1]]))

            el[2].append(l[1:])
            i += 1
            line = lines[i]
            if(j+1 == count[2]):
                break
            l = list(map(int,line.rstrip().split(' ')))
        cur += 1
        continue

    # higher elements
    for j in range(count[cur]):
        el[cur].append(l[1:])
        if(j+1 == count[cur]):
                break
        i += 1
        line = lines[i]
        l = list(map(int,line.rstrip().split(' ')))
    cur += 1

for i in edges:
    edge = []
    for j in i:
        edge.append(j)
    el[1].append(edge)


eps = 1e-9

edgesqlengths = {}

for edge in edges:
    c = 1
    edge = list(edge)
    sl = sqlength(edge)
    k = list(edgesqlengths.keys())
    for i in range(len(k)):
        if(abs(k[i] - sl) < eps):
            edgesqlengths[k[i]] += 1
            c = 0
            break
    if(c):
        edgesqlengths[sl] = 1

edgelengths = list(edgesqlengths.keys())
edgelengths.sort()
edgecounts = [edgesqlengths[i] for i in edgelengths]
edgelengths = list(map(math.sqrt, edgelengths))

'''for i in range(d):
    print(el[i])
    print(len(el[i]))
    print()'''

print("Edges:")
for i in range(len(edgelengths)):
    print(edgecounts[i], "of length", round(edgelengths[i],6))

print()