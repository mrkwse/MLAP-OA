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

    cpt = calculate_p_array(prob, parents, data_in)

    prob = calculate_m_p(prob, parents, data_in, cpt)

    pprint(cpt)
    pprint(prob)
    log_like = calc_log_likelihood(cpt, data_in, parents)
    print "log-likelihood is currently: " + str(log_like)

    cpt = calculate_p_array(prob, parents, data_in)

    # pprint(prob)
    # pprint(cpt)
    log_like = calc_log_likelihood(cpt, data_in, parents)
    print "log-likelihood is currently: " + str(log_like)

    ii = 0
    while ii < 5:
        prob = calculate_m_p(prob, parents, data_in, cpt)
        cpt = calculate_p_array(prob, parents, data_in)

        log_like = calc_log_likelihood(cpt, data_in, parents)
        print "log-likelihood is currently: " + str(log_like)

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

def calculate_consequent_p(data, column, prob, parents, cpt):
    count_1 = 0
    count_0 = 0
    count_un = 0

    for row in data:
        if row[column] == 1:
            count_1 += 1
        elif row[column] == 0:
            count_0 += 1
        else:
            if parents[column] == []:
                count_un += 1
            else:
                key = []
                ii = 0
                missing = []
                m_index = []
                for ancestor in parents[column]:
                    if row[ancestor] > -1:
                        key.append([ancestor, row[ancestor]])
                    else:
                        key.append([ancestor, []])
                        missing.append(ancestor)
                        m_index.append(ii)
                    ii += 1
                pp = 0
                yy = 0


                """
                Sum the products of probabilities from cpt
                """
                if (missing != []) and (len(missing) < len(parents)):
                    px = [1.0, 1.0]
                    while pp < math.pow(2, len(missing)):
                        xx = return_binary_array(pp, len(missing))
                        kk = 0
                        while kk < len(missing):
                            key[m_index[kk]][1] = xx[kk]
                            px[0] = px[0] * prob[m_index[kk]][xx[kk]]
                            px[1] = px[1] * prob[m_index[kk]][xx[kk]]
                            kk += 1
                        pp += 1
                        px[1] = px[1] * cpt[column][1][str(key)] * prob[column][1]
                        px[0] = px[0] * cpt[column][0][str(key)] * prob[column][0]
                    count_1 += px[1]
                    count_0 += px[0]

                # while pp < math.pow(2, len(unknown)):
                #     key = []
                #     xx = return_binary_array(pp, len(unknown))
                #     qq = 0
                #
                #     while qq < 2:
                #         px[qq] = prob[column][qq][str(key)]


    p1 = (float(count_1) / float(len(data)))
    p0 = (float(count_0) / float(len(data)))
    # p1 = (float(count_1) + (count_un * prob[column][1])) / float(len(data))
    # p0 = (float(count_0) + (count_un * prob[column][0])) / float(len(data))
    return [p0, p1]

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
            # print instance
        ii += 1
    pprint(prob)
    return prob

def calc_complex_ps(data, columns, prob):
    ii = 0
    cumulative = 0.0
    check_arr = {}

    for row in data:
        inc = 1.0
        # if (row[columns[0][0]] == columns[0][1]) or (row[columns[0][0]] == -1):
        ii += 1
        for element in columns:
            check_arr[element[0]] = 0

        for element in columns:
            if row[element[0]] == -1:
                check_arr[element[0]] = -1
            elif row[element[0]] == element[1]:
                check_arr[element[0]] = 1
            else:
                inc = 0.0

        if check_arr.values().count(0) == 0:
            if check_arr.values().count(-1) != 0:
                for element in columns:
                    if check_arr[element[0]] == -1:
                        inc = inc * prob[element[0]][element[1]]
            # if check_arr.values().count(-1) == len(columns):
            #     inc = 0.0

        cumulative += inc

    # for row in data:
    #     if row[columns[0][0]] == columns[0][1]:
    #         ii += 1

        # if inc != 0:
        #     ii += 1
                # print xx
    # print columns
    # print cumulative
    # print ii

    joint = cumulative / len(data)

    cumulative = 0.0

    for row in data:
        inc = 1.0
        jj = 1
        while jj < len(columns):
            if (row[columns[jj][0]] != columns[jj][1]) and (row[columns[jj][0]] != -1):
                inc = 0.0
            elif row[columns[jj][0]] == -1:
                inc = inc * prob[columns[jj][0]][columns[jj][1]]
            jj += 1
        cumulative += inc



    parental_joint = cumulative / len(data)

    if ii > 0:
        # print "For " + str(columns) + " count is " + str(cumulative) + " total is " + str(ii)
        return joint / parental_joint
    else:
        return 0.0

def calculate_p_array(prob, parents, data):
    ii = 0

    # for column in data[0]:
    #     # if parents[ii] == []:
    #         # pass
    #     prob[ii] = calculate_consequent_p(data, ii, prob)
    #     ii += 1


    p_array = copy.deepcopy(prob)

    ii = 0
    for column in data[0]:
        if parents[ii] != []:
            p_array[ii] = [{}, {}]
            instance = []
            for child in parents[ii]:
                instance.append(child)

            pp = 0
            xx = []

            for a in instance:
                xx.append(0)

            px = 0
            while pp < math.pow(2, (len(parents[ii]))):
                key = []
                xx = return_binary_array(pp, (len(parents[ii])))
                qq = 0
                while qq < len(instance):
                    key.append([instance[qq], xx[qq]])
                    qq += 1
                pp += 1
                ch = [[ii, 0]]
                p_arr = copy.deepcopy(key)
                p_arr[:0] = ch
                # px += calc_complex_ps(data, p_arr, pre_prob)
                p_array[ii][0][str(key)] = calc_complex_ps(data, p_arr, prob)
                p_array[ii][1][str(key)] = 1 - p_array[ii][0][str(key)]
            # prob[ii] = [px, (1-px)]
            # pprint(prob)
            # print instance

        ii += 1

    return p_array

            # prob[ii][xx]

def calc_log_likelihood(prob, data, parents):
    log_sum = 0.0
    # uncondtitional = 0.0
    for row in data:
        ii = 0
        while ii < len(row):
            px = 0.0
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
                    px1 = prob[ii][row[ii]][str(key)]
                    if px1 > px:
                        px = px1
                    # if px > 0:
                    #     log_sum += math.log(px)
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
                            xx = return_binary_array(pp, check_arr.values().count(-1))
                            qq = 0
                            while qq < check_arr.values().count(-1):
                                if missing[qq] == -1:
                                    jj = xx[qq]
                                else:
                                    key[missing[qq]][1] = xx[qq]
                                qq += 1
                            pp += 1
                            px1 = prob[ii][jj][str(key)]
                            if px1 > px:
                                px = px1
                    # else:
                    #     while pp < len(parents[ii]):
                    #         key[]
                    elif (len(missing) < len(parents[ii]) + 1):
                        px1 = prob[ii][row[ii]][str(key)]
                        if px1 > px:
                            px = px1

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

def calculate_m_p(prob, parents, data_in, cpt):
    old_prob = copy.deepcopy(prob)
    ii = 0
    for column in data_in[0]:
    #     # if parents[ii] == []:
    #         # pass
        prob[ii] = calculate_consequent_p(data_in, ii, old_prob, parents, cpt)
        ii += 1

    return prob


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
