
import math

class maximin:

    def __init__(self):
        self.utility = 0

    def alphaBetaSearch(self, state):

        maxValue = self.maxValue(state, -math.inf, math.inf)

        action = state[maxValue]

        return action


    def maxValue(self, state, alpha, beta):

        # depth = 0



        if self.terminalState() == 0:
            return self.utility

        for a in state:

            return self.utility


    def alphaBetaSeatch(self, state, alpha, beta):
        utility = 0

        return utility


    def terminalState(self):
        return True