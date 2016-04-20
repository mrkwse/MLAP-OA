import csv
import getopt
import sys
import math
from pprint import pprint

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

    print data_in
    parents = parenthood(graph)
    prob = calculate_p_initial(graph, parents, data_in)

    print parents

    # while ii < len(prob):
    #     print prob[ii]
    #     ii += 1

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

    parents = {}
    kk = 0
    while kk < len(offspring):
        parents[kk] = []
        kk += 1

    for family in offspring:
        if len(family[1]) > 0:
            for instances in family[1]:
                parents[instances].append(family[0])

    return parents

# def expectation(network, data):
    # ii = 0
    # while ii < len(data):


        # q[ii](h[ii]|v[ii]) = p(h[ii]|v[ii], theta[t-1])


def calculate_p_initial(graph, parents, data):
    prob = {}
    ii = 0
    for column in graph[0]:
        prob[ii] = []
        # print prob
        # xx is the value of x (0 or 1) for p(x)
        print ii

        if parents[ii] == []:
            prob_1 = calculate_simple_p(data, ii)
            prob[ii] = [(1 - prob_1), prob_1]
        else:
            prob[ii] = [0.5, 0.5]
            # index = len(parents[ii]) + 1
            # pX = 1 / math.pow(2,index)
            #
            # # prob[ii] = [{},{}]
            # # print prob
            # prob[ii] = []
            #
            # prob_1 = 0.1
            # xx = [0]
            # # while xx[0] <= 1:
            # #     current_prob = prob[ii]
            # #     print current_prob
            # # current_prob = current_prob[xx]
            #     # if False:
            # if len(parents[ii]) > 1:
            #     jj = 0
            #     current_prob = prob[ii]
            #     kk = 0
            #     xx = [0]
            #
            #     while xx.count(0) > 0:
            #     # while jj < len(parents[ii]):
            #
            #         # print current_prob
            #         # print 'jj' + str(jj)
            #         if xx[jj] <= 1:
            #             if len(xx) < len(parents[ii]):
            #                 xx.append(0)
            #             current_prob.append({parents[ii][jj]: []})
            #             print 'xx ' + str(xx)
            #             # print parents[ii]
            #             # print current_prob
            #             # print 'jj = ' + str(jj)
            #             # current_prob[parents[ii][jj]] = []
            #             print current_prob
            #             current_prob = current_prob[xx[jj]][parents[ii][jj]]
            #             print current_prob
            #             if len(parents[ii]) < len(xx):
            #                 kk += 1
            #             xx[kk] = 1
            #             # jj += 1
            #             print xx
            #         jj += 1
            #     if xx == 0:
            #         current_prob.append(1 - prob_1)
            #     elif xx == 1:
            #         current_prob.append(prob_1)
            # # prob[ii] = [0.2, 0.2]
            #     # xx[0] += 1
        ii += 1
    pprint(prob)
    return prob

def calculate_simple_p(training_data, column):
    count_1 = 0
    count_0 = 1
    for row in training_data:
        if row[column] == 1:
            count_1 += 1
        elif row[column] == 0:
            count_0 += 1

    return (float(count_1) / (count_1 + count_0))

def calc_log_likelihood(prob, data, parents):
    log_sum = 0
    for row in data:
        ii = 0
        while ii < len(row):
            if parents[ii] == []:
                if row[ii] > -1:
                    log_sum += math.log(prob[ii][row[ii]])
                else:
                    log_sum += math.log(0)
            else:
                likelihood = 0.0
                sum_likelihood = False
                if row[ii] > -1:
                    p_x = prob[ii][row[ii]]
                    jj = 0
                    while jj < len(parents[ii]):
                        if row[parents[ii][jj]] > -1:
                            if sum_likelihood = False:
                                p_x = p_x *
                                      prob[parents[ii][jj][row[parents[ii][jj]]]]
                        else:
                            p_x = [(p_x + prob[parents[ii][jj][0]]),
                                   (p_x + prob[parents[ii][jj][1]])]
                            sum_likelihood = True









if __name__ == "__main__":
    main()
