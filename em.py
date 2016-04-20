import csv
import getopt
import sys
import math
from pprint import pprint
import string

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
    calc_log_likelihood(prob, data_in, parents)

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

        if parents[ii] == []:
            prob_1 = calculate_simple_p(data, ii)
            prob[ii] = [(1 - prob_1), prob_1]
        else:
            # prob[ii] = [0.5, 0.5]
            prob[ii] = [{},{}]
            p_x = 0.5
            instance = []
            for child in parents[ii]:
                instance.append(child)

            pp = 0
            xx = []
            for a in instance:
                xx.append(0)

            while pp < math.pow(2,(len(parents[ii]) + 1)):
                p_x = 0.5
                key = []
                xx = return_binary_array(pp, (len(parents[ii]) + 1))
                qq = 0
                while qq < len(instance):
                    key.append([instance[qq],xx[qq + 1]])
                    if prob[instance[qq]]:
                        p_x = p_x * prob[instance[qq]][xx[qq + 1]]
                        qq += 1

                prob[ii][xx[0]][str(key)] = p_x
                pp += 1

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
                    log_sum += math.log(prob[ii][0]+ prob[ii][1])
            else:
                if row[ii] > -1:
                    vals = []
                    kkey = []
                    for ancestor in parents[ii]:
                        if row[ancestor] != -1:
                            vals.append(row[ancestor])
                            aa = 0
                            # kkey = []
                            # while aa < len(vals):
                                # if parents[ii] != []:
                            kkey.append([ancestor,vals[aa]])
                                # aa += 1
                    """
                    Will fail if cell contains nan as key simply omits that
                    cell from array of key in event of having to duplicate
                    through. Maybe some sort of flag to continue/increment ii
                    and/or increment through 0/1 for each ancestor that is
                    unknown?
                    """
                    if kkey != []:
                        print str(kkey)
                        p_x = prob[ii][row[ii]][str(kkey)]
                        log_sum += math.log(p_x)
                    # p_x = prob[ii][row[ii]][kkey]
                    # log_sum += math.log(p_x)
            ii += 1
        print log_sum
            # else:
            #     likelihood = 0.0
            #     sum_likelihood = False
            #     if row[ii] > -1:
            #         p_x = prob[ii][row[ii]]
            #         jj = 0
            #         while jj < len(parents[ii]):
            #             if row[parents[ii][jj]] > -1:
            #                 if sum_likelihood == False:
            #                     pass
            #             else:
            #                 p_x = [(p_x + prob[parents[ii][jj][0]]),
            #                        (p_x + prob[parents[ii][jj][1]])]
            #                 sum_likelihood = True




def return_binary_array(iteration_integer, length):
    binary_string = "{0:b}".format(iteration_integer)
    array = list(binary_string)
    xx = 0
    while xx < len(array):
        array[xx] = int(array[xx])
        xx += 1
    if len(array) < length:
        xx = 0
        prepend = []
        while xx < (length - len(array)):
            prepend.append(0)
            xx += 1
        array = prepend + array
    return array




if __name__ == "__main__":
    main()
