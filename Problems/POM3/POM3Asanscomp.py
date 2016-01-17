from jmoo_decision import *
from jmoo_problem import jmoo_problem

from Dependencies.jmoo_objective import *
from Helper.pom3 import pom3


class POM3Asanscomp(jmoo_problem):
    "POM3A"
    def __init__(prob):
        prob.name = "POM3Asanscomp"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
        LOWS = [0.1, 0.82, 2,  0.40, 1,   1,  0, 0, 1]
        UPS  = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True, 0), jmoo_objective("Score", False, 0, 1), jmoo_objective("Idle", True, 0, 1)]

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        else: input = [decision.value for decision in prob.decisions]
        p3 = pom3()
        output = p3.simulate(input)
        output = [output[0], output[1], output[3]]
        for i,objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        return False #no constraints