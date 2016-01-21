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


def poles_point(clusters, filename):
    def fastmap(points):
        points = [point.tolist() for point in points]
        from random import choice
        random_point = choice(points)
        from Utilities.SMOTER.smoteR import euclidean_distance
        east = sorted(points, key=lambda x: euclidean_distance(random_point, x), reverse=True)[0]
        west = sorted(points, key=lambda x: euclidean_distance(east, x), reverse=True)[0]
        return [east, west]


    from random import choice
    import pandas as pd
    df = pd.read_csv(filename)
    decisions = len([h for h in df.columns if '$<' not in h])
    objectives = len([h for h in df.columns if '$<' in h])
    df = df.values.tolist()
    training_independent = []
    for points in clusters: training_independent.extend(fastmap(points))
    # print "Poles: Length of the training independent: ", len(training_independent)
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


def median_point(clusters, filename):
    def fastmap(points):
        points = [point.tolist() for point in points]
        from random import choice
        random_point = choice(points)
        from Utilities.SMOTER.smoteR import euclidean_distance
        east = sorted(points, key=lambda x: euclidean_distance(random_point, x), reverse=True)[0]
        west = sorted(points, key=lambda x: euclidean_distance(east, x), reverse=True)[int(len(points)/2)]
        return [west]


    from random import choice
    import pandas as pd
    df = pd.read_csv(filename)
    decisions = len([h for h in df.columns if '$<' not in h])
    objectives = len([h for h in df.columns if '$<' in h])
    df = df.values.tolist()
    training_independent = []
    for points in clusters: training_independent.extend(fastmap(points))
    # print "Median: Length of the training independent: ", len(training_independent)
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


def surrogate_generate_with_SMOTE(training_independent, training_dependent, bins = 10):

    from Utilities.SMOTER.smoteR import apply_smote
    from sklearn.tree import DecisionTreeRegressor

    number_of_objectives = len(training_dependent[0])
    cart_trees = []
    for objective in xrange(number_of_objectives):
        dependent = [td[objective] for td in training_dependent]
        smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)

        cart_trees.append(DecisionTreeRegressor())
        cart_trees[objective].fit(smote_indep_training, smote_dep_testing)
    return cart_trees


def surrogate_generate(training_independent, training_dependent, SMOTE=False):
    #""" decision tree
    from sklearn.tree import DecisionTreeRegressor
    number_of_objectives = len(training_dependent[0])
    cart_trees = []

    for objective in xrange(number_of_objectives):
        cart_trees.append(DecisionTreeRegressor())
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            cart_trees[objective].fit(smote_indep_training, smote_dep_testing)
        else:
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


def surrogate_generate_LR(training_independent, training_dependent, SMOTE=False):
    from sklearn import linear_model
    number_of_objectives = len(training_dependent[0])
    linear_regression_model = []

    for objective in xrange(number_of_objectives):
        linear_regression_model.append(linear_model.LinearRegression())
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            linear_regression_model[objective].fit(smote_indep_training, smote_dep_testing)
        else:
            linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])
    return linear_regression_model


def surrogate_POMX(training_independent, training_dependent, SMOTE=False):
    from sklearn import linear_model
    number_of_objectives = len(training_dependent[0])
    linear_regression_model = [None for _ in xrange(number_of_objectives)]

    for objective in [0, 2, 3]:
        linear_regression_model[objective] = linear_model.LinearRegression()
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            linear_regression_model[objective].fit(smote_indep_training, smote_dep_testing)
        else:
            linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])

    from sklearn.tree import DecisionTreeRegressor
    for objective in [1]:
        linear_regression_model[objective] = DecisionTreeRegressor()
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            linear_regression_model[objective].fit(smote_indep_training, smote_dep_testing)
        else:
            linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])

    return linear_regression_model


def surrogate_FeatureM(training_independent, training_dependent, SMOTE=True):
    from sklearn import linear_model
    number_of_objectives = len(training_dependent[0])
    linear_regression_model = [None for _ in xrange(number_of_objectives)]
    for objective in [0, 2]:
        linear_regression_model[objective] = linear_model.LinearRegression()
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            linear_regression_model[objective].fit(smote_indep_training, smote_dep_testing)
        else:
            linear_regression_model[objective].fit(training_independent, [td[objective] for td in training_dependent])

    from sklearn.tree import DecisionTreeRegressor
    for objective in [1]:
        linear_regression_model[objective] = DecisionTreeRegressor()
        if SMOTE is True:
            from Utilities.SMOTER.smoteR import apply_smote
            dependent = [td[objective] for td in training_dependent]
            smote_indep_training, smote_dep_testing = apply_smote(training_independent, dependent)
            linear_regression_model[objective].fit(smote_indep_training, smote_dep_testing)
        else:
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

    return [round(result*100, 2) for result in results]


def get_filenames(policy):
    repeats = 10
    basename = "./Data/"
    from os import listdir
    file_names = [basename + fname for fname in listdir(basename)]
    functions = [ surrogate_generate, surrogate_generate_LR]
                 # surrogate_FeatureM]#, surrogate_POMX]



    for file_name in file_names:
        print
        for function in functions:
            temp_storage = []
            print file_name,
            for repeat in xrange(repeats):
                clusters = WHEREDataTransformation(file_name)
                training_independent, training_dependent = policy(clusters, file_name)
                testing_independent, testing_dependent = get_testing_data(training_independent, file_name)

                assert(len(testing_dependent) == len(testing_independent)), "Something is wrong"

                surogates = function(training_independent, training_dependent)

                temp_storage.append(validate_data(surogates, testing_independent, testing_dependent))

            # finding mean
            from numpy import mean
            final_answer = []
            number_of_objectives = len(temp_storage[0])
            for o in xrange(number_of_objectives):
                final_answer.append(round(mean([ts[o] for ts in temp_storage]), 3))
            print function.__name__ , "\t\t\t\t : ", final_answer

        for function in functions:
            temp_storage = []
            print file_name,
            for repeat in xrange(repeats):
                clusters = WHEREDataTransformation(file_name)
                training_independent, training_dependent = policy(clusters, file_name)
                testing_independent, testing_dependent = get_testing_data(training_independent, file_name)

                assert(len(testing_dependent) == len(testing_independent)), "Something is wrong"

                surogates = function(training_independent, training_dependent, SMOTE=True)

                temp_storage.append(validate_data(surogates, testing_independent, testing_dependent))

            # finding mean
            from numpy import mean
            final_answer = []
            number_of_objectives = len(temp_storage[0])
            for o in xrange(number_of_objectives):
                final_answer.append(round(mean([ts[o] for ts in temp_storage]), 3))
            print function.__name__ + "_SMOTE ", "\t\t\t\t : ", final_answer






where_policies = [random_point, poles_point, median_point]
# where_policies = [poles_point]
for policy in where_policies:
    print policy.__name__
    print
    get_filenames(policy)
# modify_files()
# build_historgrams(None)