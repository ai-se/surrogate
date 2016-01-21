from jmoo_problem import *
from jmoo_objective import *
from jmoo_decision import *
from math import pi, cos, sin

class c1_dtlz1(jmoo_problem):
    "Constrained DTLZ1"
    def __init__(prob, numDecs=5, numObjs=2):

        super(c1_dtlz1, prob).__init__()
        prob.name = "C1_DTLZ1_" + str(numDecs) + "_" + str(numObjs)
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
            assert(0<=decision.value <= 1), "Something is wrong"

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
        constraint_value = 1 - (objectives[-1]/0.6) - (0.5 * sum(objectives[:-1]))
        return False if constraint_value >= 0 else True

class c1_dtlz3(jmoo_problem):
    "c1_DTLZ3"
    def __init__(prob, numDecs=10, numObjs=2):
        super(c1_dtlz3, prob).__init__()
        prob.name = "C1_DTLZ3_" + str(numDecs) + "_" + str(numObjs)
        names = ["x"+str(i+1) for i in range(numDecs)]
        lows =  [0.0 for i in range(numDecs)]
        ups =   [1.0 for i in range(numDecs)]
        prob.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(numDecs)]
        prob.objectives = [jmoo_objective("f" + str(i+1), True) for i in range(numObjs)]

    def evaluate(prob,input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        k = 10
        assert(len(prob.decisions) == len(prob.objectives) + 9), "Something is wrong"
        g = 0.0

        x = []
        for i in range(0, len(prob.decisions)):
            x.append(prob.decisions[i].value)

        for i in range(len(prob.decisions) - k, len(prob.decisions)):
            g += (x[i] - 0.5)**2 - cos(20.0 * pi * (x[i] - 0.5))
        assert(k == 10), "Against the recommendation of Deb's paper"
        g = 100 * (k + g)

        f = []
        for i in range(0, len(prob.objectives)):
            f.append(1.0 + g)

        for i in range(0, len(prob.objectives)):
            for j in range(0, len(prob.objectives) - (i+1)):
                f[i] *= cos(x[j]*0.5*pi)
            if not (i == 0):
                aux = len(prob.objectives) - (i+1)
                f[i] *= sin(x[aux]*0.5*pi)

        for i in range(0, len(prob.objectives)):
            prob.objectives[i].value = f[i]

        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob, input = None):
        radius = {"3": 9, "5":12.5, "8":12.5, "10":15, "15":15}
        assert( len(prob.objectives) in [3, 5, 8, 10, 15]), "Something is wrong"
        objectives = prob.evaluate(input)
        first = sum([(x**2 - 16) for x in objectives])
        second = sum([(x**2 - radius[str(len(prob.objectives))]**2) for x in objectives])
        return False if (first * second) >= 0 else True
