from jmoo_problem import *
from jmoo_objective import *
from jmoo_decision import *
from math import pi, cos, sin

class c3_dtlz1(jmoo_problem):
    "DTLZ1"
    def __init__(prob, numDecs=5, numObjs=2):

        super(c3_dtlz1, prob).__init__()
        prob.name = "C3_DTLZ1_" + str(numDecs) + "_" + str(numObjs)
        names = ["x"+str(i+1) for i in range(numDecs)]
        lows =  [0.0 for i in range(numDecs)]
        ups =   [1.0 for i in range(numDecs)]
        prob.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(numDecs)]
        prob.objectives = [jmoo_objective("f" + str(i+1), True) for i in range(numObjs)]

    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]

        for i,decision in enumerate(prob.decisions):
            assert(0 <= decision.value <= 1), "Something is wrong"

        k = 5
        assert(len(prob.decisions) == len(prob.objectives) + 4), "Something is wrong"
        g = 0.0

        x = []
        for i in range(0, len(prob.decisions)):
            x.append(prob.decisions[i].value)

        for i in range(len(prob.decisions) - k, len(prob.decisions)):
            g += (x[i] - 0.5)**2 - cos(20.0 * pi * (x[i] - 0.5))

        g = 100 * (k + g)

        f = []
        for i in range(0, len(prob.objectives)): f.append((1.0 + g)*0.5)

        for i in xrange(len(prob.objectives)):
            for j in range(0, len(prob.objectives) - (i+1)):
                f[i] *= x[j]
            if not (i == 0):
                aux = len(prob.objectives) - (i+1)
                f[i] *= 1 - x[aux]
        for i in xrange(len(prob.objectives)):
            prob.objectives[i].value = f[i]

        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        objectives = prob.evaluate(input)
        constraints = []
        for j in xrange(len(objectives)):
            constraints.append(sum([objectives[j] + objectives[i]/0.5 - 1 for i in xrange(len(objectives))]))
        bool_contraints = [True if c >= 0 else False for c in constraints]

        return False if reduce(lambda a, b: a and b, bool_contraints) is True else True


class c3_dtlz4(jmoo_problem):
    "DTLZ4"
    def __init__(prob, numDecs=10, numObjs=2):
        super(c3_dtlz4, prob).__init__()
        prob.name = "C3_DTLZ4_" + str(numDecs) + "_" + str(numObjs)
        names = ["x"+str(i+1) for i in range(numDecs)]
        lows =  [0.0 for i in range(numDecs)]
        ups =   [1.0 for i in range(numDecs)]
        prob.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(numDecs)]
        prob.objectives = [jmoo_objective("f" + str(i+1), True) for i in range(numObjs)]

    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        k = 5
        assert(len(prob.decisions) == len(prob.objectives) + 4), "Something is wrong"
        g = 0.0
        alpha = 100.0

        x = []
        for i in range(0, len(prob.decisions)):
            x.append(prob.decisions[i].value)

        for i in range(len(prob.decisions) - k, len(prob.decisions)):
            g += (x[i] - 0.5)**2

        f = []
        for i in range(0, len(prob.objectives)):
            f.append(1.0 + g)

        for i in range(0, len(prob.objectives)):
            for j in range(0, len(prob.objectives) - (i+1)):
                f[i] *= cos((x[j]**alpha) * (pi/2.0))
            if not (i == 0):
                aux = len(prob.objectives) - (i+1)
                f[i] *= sin((x[aux]**alpha) * (pi/2.0))

        for i in range(0, len(prob.objectives)):
            prob.objectives[i].value = f[i]

        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        objectives = prob.evaluate(input)
        constraints = []
        for j in xrange(len(objectives)):
            first_term = objectives[j]**2 / 4
            second_term = sum([objectives[i] ** 2 - 1 for i, objective in enumerate(objectives) if i != j])
            constraints.append(first_term + second_term)
        bool_constraints = [True if c >= 0 else False for c in constraints]
        return False if reduce(lambda a, b: a and b, bool_constraints) is True else True