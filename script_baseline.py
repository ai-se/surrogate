from __future__ import division
import pdb

def WHEREDataTransformation(filename):
    from Utilities.WHERE.where import where
    # The Data has to be access using this attribute table._rows.cells
    import pandas as pd
    df = pd.read_csv(filename)
    headers = [h for h in df.columns if '$<' not in h]
    data = df[headers]
    clusters = where(data)

    return clusters


def line_prepender(filename):
    with open(filename, 'r+') as f:
        content = f.readlines()
        total_number_of_elements = len(content[0].split(","))
        line = ",".join(
            ["$" + str(i) for i in xrange(total_number_of_elements - 3)] + ["$<" + str(i) for i in xrange(3)])

        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + "".join(content))


def modify_files():
    basename = "./Data/"
    from os import listdir
    problem_names = [basename + folder_name + "/" for folder_name in listdir(basename)]
    repeat_names = [problem_name + repeat_name + "/" for problem_name in problem_names for repeat_name in
                    listdir(problem_name)]
    from random import randint
    file_names = [repeat_name + filename for repeat_name in repeat_names for filename in listdir(repeat_name)]
    for file_name in file_names:
        line_prepender(file_name)


def random_point(clusters, filename):
    from random import choice
    import pandas as pd
    df = pd.read_csv(filename)
    decisions = len([h for h in df.columns if '$<' not in h])
    objectives = len([h for h in df.columns if '$<' in h])
    df = df.values.tolist()
    training_independent = [choice(c).tolist() for c in clusters]
    full_data = []
    for ti in training_independent:
        assert(len(ti) == decisions), "Something is wrong"
        for element in df:
            match = True
            for t, e in zip(ti, element[:decisions]):
                if t == e: pass
                else:
                    match = False
                    break

            if match is True:
                full_data.append(element)
                break

    return [fd[:decisions] for fd in full_data], [fd[decisions:] for fd in full_data]


def surrogate_generate(training_independent, training_dependent):
    #""" decision tree
    from sklearn.tree import DecisionTreeRegressor
    number_of_objectives = len(training_dependent[0])
    cart_trees = []
    for objective in xrange(number_of_objectives):
        cart_trees.append(DecisionTreeRegressor())
        cart_trees[objective].fit(training_independent, [td[objective] for td in training_dependent])
    return cart_trees

    # svm
    # from sklearn import svm
    # number_of_objectives = len(training_dependent[0])
    # clfs = []
    # for objective in xrange(number_of_objectives):
    #     # if objective == 1: clfs.append(svm.SVC(decision_function_shape='ovo'))
    #     # else: clfs.append(svm.SVR())
    #     clfs.append(svm.SVR())
    #     clfs[objective].fit(training_independent, [td[objective] for td in training_dependent])
    # return clfs


def surrogate_generate_FM(training_independent, training_dependent):
    #""" decision tree
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
    number_of_objectives = len(training_dependent[0])
    cart_trees = []

    print len(training_dependent) ,
    # Features
    cart_trees.append(DecisionTreeClassifier())
    cart_trees[0].fit(training_independent, [td[0] for td in training_dependent])

    # Constraints Violated
    cart_trees.append(DecisionTreeClassifier())
    cart_trees[1].fit(training_independent, [td[1] for td in training_dependent])

    # For Cost
    cart_trees.append(DecisionTreeRegressor())
    cart_trees[2].fit(training_independent, [td[2] for td in training_dependent])

    return cart_trees


def surrogate_generate_LR(training_independent, training_dependent):
    from sklearn import linear_model
    number_of_objectives = len(training_dependent[0])
    linear_regression_model = []
    for objective in xrange(number_of_objectives):
        linear_regression_model.append(linear_model.LinearRegression())
        linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])
    return linear_regression_model



def surrogate_generate_test1(training_independent, training_dependent):
    from sklearn import linear_model
    number_of_objectives = len(training_dependent[0])
    linear_regression_model = [None for _ in xrange(number_of_objectives)]
    for objective in [0, 2, 3]:
        linear_regression_model[objective] = linear_model.LinearRegression()
        linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])

    from sklearn.tree import DecisionTreeRegressor
    for objective in xrange(number_of_objectives):
        linear_regression_model[objective] = DecisionTreeRegressor()
        linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])
    return linear_regression_model



def get_testing_data(training_independent, filename):
    decisions = len(training_independent[0])
    import pandas as pd
    all_data = pd.read_csv(filename).values.tolist()
    testing_data =[]
    for i, data in enumerate(all_data):
        match = []
        for ti in training_independent:
            # if all the elements of data[:decisions] is equal to ti then skips
            equal = reduce(lambda x,y: x and y, [True if t == d else False for t, d in zip(ti, data[:decisions])])
            match.append(equal)
        matching = reduce(lambda x,y: x or y, match)
        #print matching, i#, data[:decisions]  this is a match
        if matching is False: testing_data.append(data)

    # assert(len(testing_data) + len(training_independent) == len(all_data)), "Something is wrong"
    return [t[:decisions] for t in testing_data], [t[decisions:] for t in testing_data]


def build_historgrams(a):
    min_value = min(a)
    max_value = max(a)
    bins = 20
    bin_size = (max_value - min_value)/bins
    bins_list = [0 for _ in xrange(bins)]
    for aa in a:
        if int(aa/bin_size)-1 == -1:
            import pdb
            pdb.set_trace()
        bins_list[int(aa/bin_size)-1] += 1
    print bins_list, bin_size, min_value, max_value, len(a)
    return bins_list


def validate_data(surrogate, testing_independent, testing_dependent):
    objectives = len(testing_dependent[0])
    assert(len(surrogate) == objectives), "Something is wrong"
    results = []
    for o in xrange(objectives):
        prediction = [float(x) for x in surrogate[o].predict(testing_independent)]
        o_testing_dependent = [td[o] for td in testing_dependent]
        mre = []
        for i, j in zip(o_testing_dependent, prediction):
                mre.append(abs(i - j)/(float(i)+1))
                # mre.append(abs(i - j))
        results.append(round(sum(mre)/len(mre), 2))

    print "Validate Data: ", [round(result*100, 2) for result in results],


def get_filenames(policy, function=surrogate_generate_test1):
    basename = "./Data/"
    from os import listdir
    file_names = [basename + fname for fname in listdir(basename)]

    for file_name in file_names:

        clusters = WHEREDataTransformation(file_name)
        training_independent, training_dependent = policy(clusters, file_name)
        testing_independent, testing_dependent = get_testing_data(training_independent, file_name)
        baseline_training_data, baseline_testing_data = get_baseline(file_name)

        # split into independent and dependent
        objectives = len(training_dependent[0])
        baseline_training_independent = [indi[:-1*objectives] for indi in baseline_training_data]
        baseline_training_dependent = [indi[-1*objectives:] for indi in baseline_training_data]

        baseline_testing_independent = [indi[:-1*objectives] for indi in baseline_testing_data]
        baseline_testing_dependent = [indi[-1*objectives:] for indi in baseline_testing_data]

        assert(len(testing_dependent) == len(testing_independent)), "Something is wrong"

        print
        print file_name, function.__name__
        # surogates = surrogate_generate(training_independent, training_dependent)
        # surogates_baseline = surrogate_generate(baseline_training_independent, baseline_training_dependent)

        # surogates = surrogate_generate_FM(training_independent, training_dependent)

        surogates = function(training_independent, training_dependent)
        surogates_baseline = function(baseline_training_independent, baseline_training_dependent)

        validate_data(surogates, baseline_testing_independent, baseline_testing_dependent)
        print len(training_independent)
        print "Baseline"
        validate_data(surogates_baseline, baseline_testing_independent, baseline_testing_dependent)
        print len(baseline_training_independent)


def get_baseline(filename, percentage=50):
    import pandas as pd
    all_data = pd.read_csv(filename).values.tolist()
    index = [i for i in xrange(len(all_data))]
    from random import shuffle
    shuffle(index)
    boundary = int(percentage * len(all_data)/100)
    training_data = [all_data[i] for i in index[:boundary]]
    testing_data = [all_data[i] for i in index[boundary:]]

    return training_data, testing_data



get_filenames(random_point)
# modify_files()
# build_historgrams(None)