from __future__ import division
from Problems.Feature_Models.feature_model import FeatureTreeModel
from Problems.POM3.POM3A import POM3A
from Problems.POM3.POM3B import POM3B
from Problems.POM3.POM3C import POM3C
from Problems.POM3.POM3D import POM3D

from Problems.XOMO.XOMO_all import XOMO_all
from Problems.XOMO.XOMO_flight import XOMO_flight
from Problems.XOMO.XOMO_ground import XOMO_ground
from Problems.XOMO.XOMO_osp import XOMO_osp
from Problems.XOMO.XOMO_osp2 import XOMO_osp2

from Utilities.to_generate_data import generate_data


def clean_up():
    folder_name = "./Data/"
    from os import system
    system("rm -rf " + folder_name + "*")

problems = [
    # FeatureTreeModel("Web_Portal", valid_solutions=True),
    # FeatureTreeModel("eshop", valid_solutions=True),
    # FeatureTreeModel("cellphone", valid_solutions=True),
    # FeatureTreeModel("EIS", valid_solutions=True),
    FeatureTreeModel("Web_Portal"),
    FeatureTreeModel("eshop"),
    FeatureTreeModel("cellphone"),
    FeatureTreeModel("EIS"),
    POM3A(),POM3B(), POM3C(), POM3D(),
    XOMO_all(), XOMO_flight(), XOMO_ground(), XOMO_osp(), XOMO_osp2()


]

number_of_samples = 1000

for problem in problems:
    print
    filename = "./Data/" + problem.name + ".csv"
    decisions = generate_data(problem, number_of_samples)
    header = ",".join(["$"+str(i) for i in xrange(len(problem.decisions))]
                      + ["$<"+str(i) for i in xrange(len(problem.objectives))])
    f = open(filename, "w")
    f.write(header + "\n")
    for decision in decisions:
        import sys
        print ".",
        sys.stdout.flush()
        line = ""
        objectives = [round(i, 3) for i in problem.evaluate(decision)]
        line += ",".join(map(str, decision))
        line += ","
        line += ",".join(map(str, objectives))
        f.write(line + "\n")
    f.close()