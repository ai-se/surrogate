from __future__ import division
from Problems.Feature_Models.feature_model import FeatureTreeModel
from Utilities.to_generate_data import generate_data


def clean_up():
    folder_name = "./Data/"
    from os import system
    system("rm -rf " + folder_name)

problems = [
    # FeatureTreeModel("Web_Portal", valid_solutions=True),
    # FeatureTreeModel("eshop", valid_solutions=True),
    # FeatureTreeModel("cellphone", valid_solutions=True),
    # FeatureTreeModel("EIS", valid_solutions=True),
    FeatureTreeModel("Web_Portal"),
    FeatureTreeModel("eshop"),
    FeatureTreeModel("cellphone"),
    FeatureTreeModel("EIS")
]

number_of_samples = 100

for problem in problems:
    print
    filename = "./Data/" + problem.name + ".csv"
    decisions = generate_data(problem, number_of_samples)
    header = ",".join(["$"+str(i) for i in xrange(len(problem.decisions))]
                      + ["$<"+str(i) for i in xrange(len(problem.objectives))])
    f = open(filename, "w")
    f.write(header + "\n")
    for decision in decisions:
        print ".",
        line = ""
        objectives = [round(i, 3) for i in problem.evaluate(decision)]
        line += ",".join(map(str, decision))
        line += ","
        line += ",".join(map(str, objectives))
        f.write(line + "\n")
    f.close()