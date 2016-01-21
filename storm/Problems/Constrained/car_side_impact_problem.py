from jmoo_problem import *
from jmoo_objective import *
from jmoo_decision import *
from math import pi, cos, sin

class car_impact(jmoo_problem):
    "Car-Side Impact Problem"
    def __init__(prob, numDecs=10, numObjs=3):
        super(car_impact, prob).__init__()
        prob.name = "Car_Impact_" + str(numDecs) + "_" + str(numObjs)
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
            g += (x[i] - 0.5)*(x[i] - 0.5)
        f = []
        for i in range(0, len(prob.objectives)):
            f.append(1.0 + g)

        for i in range(0, len(prob.objectives)):
            for j in range(0, len(prob.objectives) - (i+1)):
                f[i] *= cos(x[j]*0.5*pi);
            if not (i == 0):
                aux = len(prob.objectives) - (i+1)
                f[i] *= sin(x[aux]*0.5*pi)

        for i in range(0, len(prob.objectives)):
            prob.objectives[i].value = f[i]

        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        objectives = prob.evaluate(input)
        if len(prob.objectives) == 3: r = 0.4
        else: r = 0.5

        temp_list = []
        for i in xrange(len(objectives)):
            temp_value = (objectives[i] - 1)**2
            temp_value += sum([objectives[j] - r**2 for j in xrange(len(objectives)) if i != j])
            temp_list.append(temp_value)
        first_term = min(temp_list)
        second_term = sum([(o - (len(objectives) ** -0.5)) ** 2 for o in objectives])
        result = -1 * min(first_term, second_term)

        return False if result >= 0 else True