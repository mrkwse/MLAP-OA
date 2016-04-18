import csv
import getopt
import sys

def main(argv=None):

    if argv == None:
        argv = sys.argv

    prob = []

    try:
        with open (argv[1], 'rb') as csvfile:
            reader = csv.reader(csvfile)

            graph = []

            for row in reader:
                node = []
                for element in row:
                    node.append(int(element))
                graph.append(node)
    except Exception as e:
        raise

    try:
        with open (argv[2], 'rb') as csvfile:
            reader = csv.reader(csvfile)

            data_in = []

            for row in reader:
                node = []
                for element in row:
                    if element != 'nan':
                        node.append(int(element))
                    else:
                        node.append(-1) # Check solution for unknown var
                data_in.append(node)
    except Exception as e:
        raise

    ii = 0

    prob = calculate_p(graph)
    parents = parenthood(graph)

    print parents

    while ii < len(prob):
        print prob[ii]
        ii += 1

def parenthood(network):
    offspring = []
    ii = 0
    for row in network:
        ancestor = [ii, []]
        jj = 0
        for x in row:

            if x == 1:
                ancestor[1].append(jj)
            jj += 1

        offspring.append(ancestor)
        ii += 1

    parents = []
    kk = 0
    while kk < len(offspring):
        parents.append([kk, []])
        kk += 1

    for family in offspring:
        if len(family[1]) > 0:
            for instances in family[1]:
                parents[instances][1].append(family[0])

    return parents

def expectation(network, data):
    ii = 0
    # while ii < len(data):


        # q[ii](h[ii]|v[ii]) = p(h[ii]|v[ii], theta[t-1])


def calculate_p(data):
    prob = []
    for row in data:
        row_p = []
        xx = 0
        while xx < len(row):
            if row[xx] == 1:
                row_p.append([[0.5, 0.5], [0.5, 0.5]])
            else:
                row_p.append(0)
            xx += 1
        prob.append(row_p)
    # print prob
    return prob






if __name__ == "__main__":
    main()
