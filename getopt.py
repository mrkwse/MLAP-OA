import csv
import getopt
import sys

def main(argv=None):
    # csv_in = getopt.getopt(argv, ':')
    if argv == None:
        argv = sys.argv

    try:
        with open (argv[1], 'rb') as csvfile:
            reader = csv.reader(csvfile) #, lineterminator='\n')

            graph = []

            for row in reader:
                node = []
                for element in row:
                    node.append(int(element))
                graph.append(node)

            ii = 0
            while (ii < len(graph)):
                print graph[ii]
                ii += 1
            # print len(graph)
            # print len(graph[0])

    except Exception as e:
        raise

    graph_dimensions = {'x': len(graph[0]), 'y': len(graph)}

    # TODO step 0
    """
    Moralise!
    0. Check if graph directed
    1a. Transpose (with 2s)
    2. Join parents (bidirectional)
    1b. Replace transposed 2s with 1s
    """

    print "transpose!"
    # transposition step
    ii = 0
    while (ii < len(graph)):
        jj = 0
        while (jj < len(graph[ii])):
            if (graph[ii][jj] == 1):
                graph[jj][ii] = 2
            jj = jj + 1
        print graph[ii]
        ii = ii + 1

    """
    Joining parents.
    First create a list containing a list of children, paired with a
    list of parents.
    E.g. [[child1, [parent1, parent2]], [child2, [parent1, parent2]], ...]
    """
    child_parent = []
    yy = 0
    while yy < len(graph):
        xx = 0
        if graph[yy].count(2) > 0:
            child = [yy,[]]
            while (xx < len(graph[yy])):
                if (graph[yy][xx] == 2):
                    child[1].append(xx)
                xx += 1
            child_parent.append(child)
        yy += 1
    print child_parent

    """
    Write 1s for each edge to/from each parent node.
    """
    ii = 0
    parent_edges = []
    while ii < len(child_parent):
        if child_parent[ii][1] > 1:
            jj = 0
            while jj < len(child_parent[ii][1]):
                kk = 0
                while kk < len(child_parent[ii][1]):
                    if kk != jj:
                        parent_edges.append([child_parent[ii][1][jj],
                                             child_parent[ii][1][kk]])
                    kk += 1
                jj += 1
        ii += 1

    print parent_edges
    ii = 0
    while ii < len(parent_edges):
        graph[parent_edges[ii][0]][parent_edges[ii][1]] = 1
        ii += 1

    ii = 0
    while (ii < len(graph)):
        jj = 0
        while (jj < len(graph[ii])):
            if (graph[ii][jj] == 2):
                graph[ii][jj] = 1
            jj = jj + 1
        print graph[ii]
        ii = ii + 1

    """
    Moralisation complete!
    """

    """
    Triangulation goes in here
    """

    print "triangulation"
    print len(graph)
    ii = 0
    while ii < len(graph):
        xx = 0
        yy = ii
        parents = []
        first_branch = []
        start = True
        jj = 0
        while xx <= len(graph[yy]):
            # print 'loop1'
            if xx == len(graph[yy]):
                # print 'ifjj'
                start = True
                jj += 1

                if jj < len(graph):
                    # print 'iflng'
                    yy = jj
                    xx = 0
                else:
                    print first_branch
                    xx += 1
            else:
                # print 'elsejj'
                if parents.count(xx) > 0:
                    # print 'ifparents'
                    xx += 1
                else:
                    # print 'elseparents'
                    if first_branch.count(xx) > 0:
                        # print 'iffb'
                        xx += 1
                    else:
                        # print 'elsefb'
                        if graph[yy][xx] == 1:
                            # print 'ifgyx'
                            parents.append(yy)
                            if start == True:
                                # print 'ifstart'
                                first_branch.append(xx)
                                start = False
                            yy = xx
                            xx = 0
                            # xx = len(graph[yy])
                        else:
                            # print 'elsegyx'
                            xx += 1
        print parents
        print 'xx: ' + str(xx) + ' yy: ' + str(yy) + ' ii: ' + str(ii)
        ii += 1



    print "Junction trees"

    ii = len(graph)
    print 'ii:' + str(ii)
    while (ii > 0):
        ii -= 1
        print 'ii- : ' + str(ii)
        jj = len(graph[0])
        print 'jj:' + str(jj)
        while (jj > 0):
            jj -= 1
            if (ii == jj):
                pass
                print 'equal'
            else:
                print 'not sure'
                if (graph[ii][jj] == 0):
                    print 'pop row: ' + str(ii)
                    graph.pop(jj)
                    for rows in graph[jj]:
                        print rows

    for rows in graph:
        print rows

if __name__ == "__main__":
    main()
