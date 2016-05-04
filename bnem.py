#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

    parents = parenthood(graph)
    conditional_data = copy.deepcopy(data_in)
    prob = calculate_p_initial(graph, parents, data_in)
    steps = 0

    conditional_data = e_step(prob, conditional_data, data_in, parents)
    cpt = m_step(conditional_data, parents, data_in)
    steps += 1

    log_like = calc_log_likelihood(cpt, data_in, parents)
    print "log-likelihood is currently: " + str(log_like)

    conditional_data = e_step(cpt, conditional_data, data_in, parents)
    cpt = m_step(conditional_data, parents, data_in)
    conditional_data = e_step(cpt, conditional_data, data_in, parents)

    delta = 10.0
    while delta > 0.0001:
        log_like_previous = log_like
        conditional_data = e_step(cpt, conditional_data, data_in, parents)
        cpt = m_step(conditional_data, parents, data_in)
        

        log_like = calc_log_likelihood(cpt, data_in, parents)
        print "log-likelihood is currently: " + str(log_like)

        delta = log_like - log_like_previous

        steps += 1

    print ""
    print "Convergence in " + str(steps) + " steps"

    print_var(cpt, parents)

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

def calculate_p_initial(graph, parents, data, starting_p=None):
    prob = {}
    ii = 0
    for column in graph[0]:
        prob[ii] = []

        if starting_p == None:
            prob_1 = 0.5

        if parents[ii] == []:
            prob[ii] = [(1 - prob_1), prob_1]
        else:
            aa = 0
            prob[ii] = [{}, {}]

            while aa < math.pow(2,len(parents[ii])):
                xval = return_binary_array(aa, len(parents[ii]))
                key = []

                jj = 0
                for ancestor in parents[ii]:
                    key.append([ancestor, xval[jj]])
                    jj += 1

                prob[ii][0][str(key)] = (1 - prob_1)
                prob[ii][1][str(key)] = prob_1

                aa += 1

        ii += 1

    return prob

def calc_log_likelihood(prob, data, parents):
    log_sum = 0.0   # Log-Likelihood sum

    # Iterate through every row of instances
    for row in data:
        ii = 0  # used to iterate through column of row and allow easier indexing
        while ii < len(row):
            # px = 0.0    #
            if parents[ii] == []:   # Logic to check if element is unconditional
                if row[ii] > -1:    # Check that row determined
                    if (prob[ii][row[ii]]) > 0: # check to avoid log(0)
                        log_sum += math.log(prob[ii][row[ii]])  # Add log(prob of element = instance) to likelihood sum
                else:
                    log_sum += math.log((prob[ii][0] + prob[ii][1])) # Add sum log(prob of element = 1 or 0) to likelihood sum
            else:
                check_arr = {}  # Array to allow easier looping
                if row[ii] == -1:   # If the element is unknown (?)
                    check_arr[ii] = -1  # Set the corresponding element in the check_arr dict to -1

                for element in parents[ii]: # Iterate through parents
                    check_arr[element] = 0
                for element in parents[ii]:
                    if row[element] == -1:
                        check_arr[element] = -1
                if check_arr.values().count(-1) == 0:
                    key = []
                    for element in parents[ii]:
                        key.append([element, row[element]])
                    px = prob[ii][row[ii]][str(key)]
                    if px1 > px:
                        px = px1
                    if px > 0:
                        log_sum += math.log(px)
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

                    if (missing != []):
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
                            if px1 < px:
                                px = px1
                    else:
                        px1 = prob[ii][jj][str(key)]
                        px = px1

                if px > 0:
                    log_sum += math.log(px)

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

def e_step(cpt, conditional_data, data_in, parents):

    # Count of which row is currently being used
    yy = 0


    # Iterate through each row
    for row in data_in:

        # Create array to track unknown elements in a particular row
        unknown_elements = []

        # Count of which element (column/variable) is currently indexed
        ii = 0

        # Iterate through row and note which variables are unknown
        for element in row:
            if element == -1:
                unknown_elements.append(ii)
            ii += 1

        ii = 0

        # Iterate through unknown elements/variables
        for element in unknown_elements:

            # Initialize (figuratively) arrays (& dicts) to store probabilities
            conditional_data[yy][unknown_elements[ii]] = [0.0, 0.0]

            # Variables to track the sums of the likelihood of either case
            # (0 or 1) across all possible permuatations of the missing
            # elements in a row
            sum_prod_0 = 0.0
            sum_prod_1 = 0.0

            # Track combined likelihood of 0 or 1 to calculate probabilities
            # from later
            sum_prod_sum = 0.0


            # Count to iterate through all permutations of missing variables
            aa = 0

            # Iterate through all permutations of the missing variable
            while aa < math.pow(2, len(unknown_elements)):

                # Track the current product of the probabilities of each
                # variable
                product = 1.0

                # Return the current permutations as a binary array
                xval = return_binary_array(aa, len(unknown_elements))

                # Count to iterate through each element
                xx = 0

                # Iterate through each element
                for value in row:

                    # Check if current element is unconditional
                    if parents[xx] == []:

                        # If current unconditional element is unknown, use
                        # current permutation to look up probability, otherwise
                        # use actual value
                        if value == -1:
                            product = product * cpt[xx][xval[unknown_elements.index(xx)]]
                        else:
                            product = product * cpt[xx][value]


                    else: # elif current element is conditional

                        # Store the intersection of parents that are not
                        # known variables/elements
                        unknown_parents = list(set(unknown_elements) & set(parents[xx]))

                        # Array to generate key to look up conditional
                        # probabilities
                        key = []

                        # Check if any parents need to be filled in
                        if len(unknown_parents) == 0:
                            # Parents known, populate key with known values
                            for ancestor in parents[xx]:
                                key.append([ancestor, row[ancestor]])
                            # If actual element unknown, lookup index of cpt
                            # from current permutation, otherwise use actual value
                            if value == -1:
                                product = product * cpt[xx][xval[unknown_elements.index(xx)]][str(key)]
                            else:
                                product = product * cpt[xx][value][str(key)]
                        else:
                            # Populate key with real or permutation value
                            for ancestor in parents[xx]:
                                if row[ancestor] != -1:
                                    key.append([ancestor, row[ancestor]])
                                else:
                                    key.append([ancestor, xval[unknown_elements.index(ancestor)]])
                            # Calculate product according to key and real/permulation
                            # probability in cpt
                            if value == -1:
                                product = product * cpt[xx][xval[unknown_elements.index(xx)]][str(key)]
                            else:
                                product = product * cpt[xx][value][str(key)]
                    xx += 1

                # Add the product to the relevant sum
                if row[element] == 0:
                    sum_prod_0 += product
                elif row[element] == 1:
                    sum_prod_1 += product
                else:
                    if xval[unknown_elements.index(element)] == 0:
                        sum_prod_0 += product
                    else:
                        sum_prod_1 += product

                sum_prod_sum += product

                aa += 1

            # Return conditional data (BN) according to current value, with
            # conditional value calculated as sum of product for that value
            # over total sum of products
            conditional_data[yy][unknown_elements[ii]][0] = sum_prod_0 / sum_prod_sum
            conditional_data[yy][unknown_elements[ii]][1] = sum_prod_1 / sum_prod_sum

            ii += 1

        yy += 1


    return conditional_data


def m_step(conditional_data, parents, data_in):

    # Define new cpt to write new values to
    cpt = {}

    # Counting variable to iterate through conditional_data array
    ii = 0

    # Iterate through every column (i.e. variable)
    for column in conditional_data[0]:

        # Instantiate key for current variable to have two values, for 0 and 1
        cpt[ii] = [0,0]

        # Count of instances (or probability) x==0
        count_0 = 0.0

        # Count of instances (or probability) x==1
        count_1 = 0.0

        # Instances (or probability) parental variables match current array
        count_ancestral = 0.0

        # Counting variable for every row of instances of all variables
        jj = 0

        # Case for unconditional variables
        if parents[ii] == []:

            # Loop through every row (instance of variable)
            while jj < len(conditional_data):

                # Add one to count of 0s if the value of element [jj][ii] is 0
                if conditional_data[jj][ii] == 0:
                    count_0 += 1

                # Add one to count of 1s if value of element [jj][ii] is 1
                elif conditional_data[jj][ii] == 1:
                    count_1 += 1

                # If element [jj][ii] is unknown (-1), add the probability of
                # it being 0 or 1 to the respective counts.
                else:
                    count_0 += conditional_data[jj][ii][0]
                    count_1 += conditional_data[jj][ii][1]

                # Increment row count
                jj += 1

            # After iterating through every row, divide count of either
            # variable value by total count of the unconditional variable
            cpt[ii][0] = count_0 / len(conditional_data)
            cpt[ii][1] = count_1 / len(conditional_data)

        # Case for conditional variables
        else:

            # Create key for current variable containing a dictionary for either
            # var=0 or var=1 (with index of dictionary representing value of
            # variable)
            cpt[ii] = [{},{}]

            # Count to iterate through every possible combination of 0s and 1s
            # in the parents of current variable
            p_in = 0

            # Loop through following for as many permutations of 0s and 1s
            # that exist (i.e., 2^n, where n = number of parents) in parents
            # variables
            while p_in < math.pow(2, len(parents[ii])):

                # List to store parents and values of each parent variable
                # throughout iterations
                key = []

                # Count of instances (or probability) x==0
                count_0 = 0.0

                # Count of instances (or probability) x==1
                count_1 = 0.0

                # Count of instances (or probability) where the parents
                # variables match (or may match) the currently defined values
                # of each parent
                count_ancestral = 0.0

                # Convert current iteration count into a binary array
                # representing which parents equal 0 or 1.
                xval = return_binary_array(p_in, len(parents[ii]))

                # Count to iterate through each parent and generate the key
                kk = 0

                # Loop through each parent and generate key from binary array
                # xval
                while kk < len(parents[ii]):
                    key.append([parents[ii][kk], xval[kk]])
                    kk += 1

                # Count to iterate through each row of the input data
                jj = 0

                # Iterate through each row
                for row in data_in: #FIXME replace data_in with conditional_data?

                    # Count to iterate through parents to check instance value
                    # against current key value
                    ll = 0

                    # Value to increment counts by (starts at 1.0 to take
                    # product of probabilities of variables occurring)
                    inc = 1.0

                    # Bool to ensure only valid (X=x or X=-1) instances
                    # contribute to counts
                    valid = True

                    # Iterate through parents
                    while ll < len(parents[ii]):

                        # Check if instance is invalid (X!=xval or X!=-1)
                        if (row[parents[ii][ll]] != xval[ll]) and (row[parents[ii][ll]] != -1):
                            inc = 0.0
                            valid = False

                        # If the instance is -1, use product as count increment
                        elif (row[parents[ii][ll]] == -1):
                            inc = inc * conditional_data[jj][parents[ii][ll]][xval[ll]]
                        ll += 1

                    # If instance is valid, increment corresponding values
                    if valid:
                        if row[ii] == 0:
                            count_0 += inc
                            count_ancestral += inc
                        elif row[ii] == 1:
                            count_1 += inc
                            count_ancestral += inc
                        else:
                            if isinstance(conditional_data[jj][ii][0], dict):
                                count_0 += conditional_data[jj][ii][0][str(key)] * inc
                                count_1 += conditional_data[jj][ii][1][str(key)] * inc
                                count_ancestral += inc
                            else:
                                count_0 += conditional_data[jj][ii][0] * inc
                                count_1 += conditional_data[jj][ii][1] * inc
                                count_ancestral += inc

                    jj += 1

                # Calculate cpt from count of corresponding value over total
                # occurances of ancestor
                cpt[ii][0][str(key)] = count_0 / count_ancestral
                cpt[ii][1][str(key)] = count_1 / count_ancestral
                p_in += 1


        ii += 1

    return cpt


def return_unknown_parents(row, ancestors):
    unknown_parents = []
    for ancestor in ancestors:
        if (row[ancestor] != 0) and (row[ancestor] != 1):
            unknown_parents.append(ancestor)

    return unknown_parents

def print_var(cpt, parents):
    ii = 0
    childval = 1
    for key in cpt.keys():
        parental_str = "("

        for ancestor in parents[key]:
            parental_str += str(ancestor) + ', '
        if parental_str != "(":
            parental_str = parental_str[:-2]
        parental_str += ")"
        print "Variable " + str(key) + " has these parents " + parental_str

        pp = 0

        while pp < math.pow(2, len(parents[ii])):
            xx = return_binary_array(pp, len(parents[ii]))

            key_parent = []
            qq = 0
            while qq < len(parents[ii]):
                key_parent.append([parents[ii][qq], xx[qq]])
                qq += 1

            exes = ""
            px = 0
            if key_parent != []:
                for x_in in xx:
                    exes += "'" +  str(x_in) + "', "
                if exes != "":
                    exes = exes[:-2]

                px = cpt[key][1][str(key_parent)]
            else:
                px = cpt[key][1]
            print "P(" + str(key) + "=" + str(childval) + "|(" + exes + ")) = " + str(px)
            pp += 1

        print ""
        ii += 1

if __name__ == "__main__":
    main()
