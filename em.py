import csv
import getopt
import sys
import math
from pprint import pprint
import string
import copy

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

    # print data_in
    parents = parenthood(graph)
    prob = calculate_p_initial(graph, parents, data_in)
    # prob = calculate_init_array(prob, parents, data_in)
    # log_like = calc_log_likelihood(prob, data_in, parents)

    pprint(prob)
    print parents
    # print graph
    # print "log-likelihood is currently: " + str(log_like)

    prob = calculate_p_array(prob, parents, data_in)
    log_like = calc_log_likelihood(prob, data_in, parents)
    print "log-likelihood is currently: " + str(log_like)

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

def calculate_p_initial(graph, parents, data):
    prob = {}
    ii = 0
    for column in graph[0]:
        prob[ii] = []
        # print prob
        # xx is the value of x (0 or 1) for p(x)

        # if parents[ii] == []:
        prob_1 = calculate_simple_p(data, ii)
        prob[ii] = [(1 - prob_1), prob_1]
        # else:
        #     # prob[ii] = [0.5, 0.5]
        #     prob[ii] = [{},{}]
        #     p_x = 0.5
        #     instance = []
        #     for child in parents[ii]:
        #         instance.append(child)
        #
        #     pp = 0
        #     xx = []
        #     for a in instance:
        #         xx.append(0)
        #
        #     while pp < math.pow(2,(len(parents[ii]) + 1)):
        #         p_x = 0.5
        #         key = []
        #         xx = return_binary_array(pp, (len(parents[ii]) + 1))
        #         qq = 0
        #         while qq < len(instance):
        #             key.append([instance[qq],xx[qq + 1]])
        #             if prob[instance[qq]]:
        #                 p_x = p_x * prob[instance[qq]][xx[qq + 1]]
        #                 qq += 1
        #
        #         prob[ii][xx[0]][str(key)] = p_x
        #         pp += 1

        ii += 1
    # pprint(prob)
    return prob

def calculate_simple_p(training_data, column):
    count_1 = 0
    count_0 = 0
    for row in training_data:
        if row[column] == 1:
            count_1 += 1
        elif row[column] == 0:
            count_0 += 1

    # return (float(count_1) / (count_1 + count_0))
    return 0.5

def calculate_consequent_p(data, column, prob):
    count_1 = 0
    count_0 = 0
    count_un = 0

    for row in data:
        if row[column] == 1:
            count_1 += 1
        elif row[column] == 0:
            count_0 += 1
        else:
            count_un += 1
    p1 = (float(count_1) + (count_un * prob[column][1])) / len(data)
    p0 = (float(count_0) + (count_un * prob[column][0])) / len(data)
    return [p0, p1]

def calc_complex_ps(data, columns, prob):
    ii = 0
    xx = 0
    check_arr = {}

    for row in data:
        for element in columns:
            check_arr[element[0]] = 0
        for element in columns:
            if row[element[0]] == -1:
                check_arr[element[0]] = -1
            elif row[element[0]] == element[1]:
                check_arr[element[0]] = 1

        if check_arr.values().count(0) == 0:
            if check_arr.values().count(-1) == 0:
                xx += 1
            else:
                pp = 1.0
                jj = 0
                for element in columns:
                    if check_arr[element[0]] == -1:
                        pp = pp * prob[element[0]][element[1]]
                xx += pp
                print xx
    return xx / len(data)

def calculate_init_array(prob, parents, data):
    ii = 0
    pre_prob = copy.deepcopy(prob)
    for column in data[0]:
        if parents[ii] != []:
            prob[ii] = [{}, {}]
            instance = []
            for child in parents[ii]:
                instance.append(child)

            pp = 0
            xx = []

            for a in instance:
                xx.append(0)

            px = 0

            while pp < math.pow(2, (len(parents[ii]) + 1)):
                key = []
                xx = return_binary_array(pp, (len(parents[ii]) + 1))
                qq = 0
                while qq < len(instance):
                    key.append([instance[qq], xx[qq+1]])
                    qq += 1
                pp += 1
                # ch = [[ii, xx[0]]]
                # p_arr[:0] = ch
                prob[ii][xx[0]][str(key)] = 0.5
            # pprint(prob)
            print instance
        ii += 1
    pprint(prob)
    return prob

def calculate_p_array(prob, parents, data):
    ii = 0
    pre_prob = copy.deepcopy(prob)
    for column in data[0]:
        if parents[ii] == []:
            prob[ii] = calculate_consequent_p(data, ii, prob)
        else:
            # xx = 0
            # while xx < 2:
            #     p0 = 0.0
            #     p1 = 0.0
            prob[ii] = [{}, {}]
            instance = []
            for child in parents[ii]:
                instance.append(child)

            pp = 0
            xx = []

            for a in instance:
                xx.append(0)

            px = 0
            while pp < math.pow(2, (len(parents[ii]) + 1)):
                key = []
                xx = return_binary_array(pp, (len(parents[ii]) + 1))
                qq = 0
                while qq < len(instance):
                    key.append([instance[qq], xx[qq+1]])
                    qq += 1
                pp += 1
                ch = [[ii, xx[0]]]
                p_arr = copy.deepcopy(key)
                p_arr[:0] = ch
                # px += calc_complex_ps(data, p_arr, pre_prob)
                prob[ii][xx[0]][str(key)] = calc_complex_ps(data, p_arr, pre_prob)
            # prob[ii] = [px, (1-px)]
            pprint(prob)
            print instance

        ii += 1

    return prob

            # prob[ii][xx]

def calc_log_likelihood(prob, data, parents):
    log_sum = 0.0
    # uncondtitional = 0.0
    for row in data:
        ii = 0
        while ii < len(row):
            if parents[ii] == []:
                if row[ii] > -1:
                    if (prob[ii][row[ii]]) > 0:
                        log_sum += math.log(prob[ii][row[ii]])
                else:
                    log_sum += math.log((prob[ii][0] + prob[ii][1]))
            else:
                check_arr = {}
                if row[ii] == -1:
                    check_arr[ii] = -1

                for element in parents[ii]:
                    check_arr[element] = 0
                for element in parents[ii]:
                    if row[element] == -1:
                        check_arr[element] = -1
                if check_arr.values().count(-1) == 0:
                    key = []
                    for element in parents[ii]:
                        key.append([element, row[element]])
                    px = prob[ii][row[ii]][str(key)]
                    if px > 0:
                        math.log(px)
                else:
                    key = []
                    mm = 0
                    missing = []
                    if row[ii] == -1:
                        missing.append(-1)
                    for element in parents[ii]:
                        if row[element] > -1:
                            key.append([element, row[element]])
                        else:
                            key.append([element, []])
                            missing.append(mm)
                        mm += 1
                    pp = 0
                    jj = row[ii]
                    px = 0.0
                    # TODO
                    # pdb break here and step through to check summation of prob
                    if (missing != []) and (len(missing) < len(parents[ii]) + 1):
                        while pp < math.pow(2, check_arr.values().count(-1)):
                            # key = [[]] * (len(parents[ii]) + 1)
                            xx = return_binary_array(pp, check_arr.values().count(-1))
                            qq = 0
                            while qq < check_arr.values().count(-1):
                                if missing[qq] == -1:
                                    jj = xx[qq]
                                else:
                                    key[missing[qq]][1] = xx[qq]
                                qq += 1
                            pp += 1
                            px += prob[ii][jj][str(key)]
                    # else:
                    #     while pp < len(parents[ii]):
                    #         key[]
                    elif (len(missing) < len(parents[ii]) + 1):
                        px += prob[ii][row[ii]][str(key)]
                    if px > 0:
                        log_sum += math.log(px)


                # else:
                #     pass
                #     uncondtitional += math.log(prob[ii][row[ii]])
                #     log_sum += math.log(prob[ii][0]+ prob[ii][1])
            # else:
                    # print log_sum
            ii += 1

    return log_sum
    # print "uncondtitional is currently: " + str(uncondtitional)



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
