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

    print "Moralizing step"

    ii = 0
    while (ii < len(graph)):
        jj = ii
        while (jj < len(graph[ii])):
            if (graph[ii][jj] == 1):
                graph[jj][ii] = 1
            jj = jj + 1
        print graph[ii]
        ii = ii + 1

    """
    Triangulation goes in here
    """

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
