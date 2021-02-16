import math

def sqlength(edge): # returns squared length of an edge given as a list or set of 2 elements
    global el
    global d
    a = 0
    
    v1 = min(edge)
    v2 = max(edge)
    for i in range(d):
        a += (el[0][v1][i] - el[0][v2][i])**2

    return a

def rect(length): # "general rectification" per GAP
    global el
    global d

    def midpoint(edge):
        return [(el[0][edge[0]][i]-el[0][edge[1]][i])/2 for i in range(d)]

    o = []
    sl = length**2

    for edge in el[1]:
        if(edge[2] - sl < eps):
            o.append(midpoint(edge))
    
    return o

suffix_shape = ["", "telon", "gon", "hedron", "choron", "teron", "peton", "exon", "zetton", "yotton", "xennon", "dakon", "hendon", "dokon", "tradakon", "tedakon", "pedakon", "exdakon", "zedakon", "yodakon", "nedakon", "ikon", "ikenon", "ikodon", "iktron"]
suffix_elements = ["vertices", "edges", "faces", "cells", "tera", "peta", "exa", "zetta", "yotta", "xenna", "daka", "henda", "doka", "tradaka", "tedaka", "pedaka", "exdaka", "zedaka", "yodaka", "nedaka", "ika", "ikena", "ikoda", "iktra"]

eps = 1e-9 # epsilon for float comparisons


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

            if(j+1 == count[0]):
                break
            i += 1
            line = lines[i]
            l = list(map(float,line.rstrip().split(' ')))
        cur += 1
        continue

    if(cur == 2): # faces
        for j in range(count[2]):
            for k in range(1, l[0]):
                edges.add(frozenset([l[k],l[k+1]]))
            edges.add(frozenset([l[1],l[-1]]))

            el[2].append(l) #includes count

            if(j+1 == count[2]):
                break
            i += 1
            line = lines[i]
            l = list(map(int,line.rstrip().split(' ')))
        cur += 1
        continue

    # higher elements
    for j in range(count[cur]):
        el[cur].append(l) #includes count
        if(j+1 == count[cur]):
                break
        i += 1
        line = lines[i]
        l = list(map(int,line.rstrip().split(' ')))
    cur += 1

for i in edges: # copies the set of edges to el[1]
    edge = []
    for j in i:
        edge.append(j)
    el[1].append(edge)


edgesqlengths = {}

for edge in el[1]:
    c = 1
    #edge = list(edge)
    sl = sqlength(edge)
    edge.append(sl)
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

print(suffix_elements[0].capitalize()+":")
print(count[0])
print()

print(suffix_elements[1].capitalize()+":")
for i in range(len(edgelengths)):
    print(edgecounts[i], "of length", round(edgelengths[i],6))
print()

for r in range(2,d):
    elfacetcounts = {}
    for element in el[r]:
        if(element[0] in elfacetcounts):
            elfacetcounts[element[0]] += 1
        else:
            elfacetcounts[element[0]] = 1
    
    facetcounts = list(elfacetcounts.keys())
    facetcounts.sort()
    elementcounts = [elfacetcounts[i] for i in facetcounts]

    print(suffix_elements[r].capitalize()+":")
    for i in range(len(facetcounts)):
        print(str(elementcounts[i]) + " × " + str(facetcounts[i]) + "-" + str(suffix_shape[r]))
    
    print()

out = open("output.txt", "w")

r = rect(edgelengths[int(input())-1])
for i in r:
    #print(i)
    k=1
    for j in i:
        out.write(str(j))
        if(k!=d):
            out.write(' ')
        k+=1
    out.write('\n')