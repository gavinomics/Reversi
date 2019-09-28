    #
    # def alphaBetaSearch(self, depth, state, alpha, beta):
    #
    #     if depth == 5 or self.noMoreMoves(state):
    #         value = self.getUtility(state)  # this variable just for printing
    #         print(f"Score: {value}")
    #         return self.getUtility(state)
    #
    #     maxValue = self.maxValue(state, -math.inf, math.inf)
    #
    #     action = state[maxValue]
    #
    #     return action
    #
    #
    # def maxValue(self, depth, state, alpha, beta):
    #
    #     utility = -math.inf
    #
    #     if depth == 5 or self.noMoreMoves():
    #         return utility
    #
    #     for a in validStates(state):
    #
    #
    #     return utility
    #
    # def getUtility(self, state):
    #     score = 0;
    #     for i in range(8):
    #         for j in range(8):
    #             if (state[i][j] == self.player):
    #                 score += 1
    #     return score
    #
    #
    # def noMoreMoves(self, state):
    #     for i in range(8):
    #         for j in range(8):
    #             if state[i][j] == 0:
    #                 return True
    #
    #     return False
    #
    #
    # def getResults(self, state, move, player):
    #     futureState = copy.deepcopy(state)
    #     futureState[move[0]][move[1]] = player
    #     self.flipThePieces(futureState, move, player, 1, 0)
    #     self.flipThePieces(futureState, move, player, 1, 1)
    #     self.flipThePieces(futureState, move, player, 0, 1)
    #     self.flipThePieces(futureState, move, player, -1, 1)
    #     self.flipThePieces(futureState, move, player, -1, 0)
    #     self.flipThePieces(futureState, move, player, -1, -1)
    #     self.flipThePieces(futureState, move, player, 0, -1)
    #     self.flipThePieces(futureState, move, player, 1, -1)
    #
    #     return futureState
    #
    # def flipThePieces(self, futureState, move, player, moveRow, moveColumn):
    #     row = move[0]
    #     column = move[1]
    #     continuous = True
    #     possibleFlip = []
    #     while (True):
    #         row += moveRow
    #         column += moveColumn
    #         if (row > 7 or row < 0 or column > 7 or column < 0):
    #             break
    #         elif (futureState[row][column] == 0):
    #             break
    #         elif (futureState[row][column] == player and continuous):
    #             break
    #         elif (futureState[row][column] != player):
    #             continuous = False
    #             possibleFlip.append([row, column])
    #         elif (futureState[row][column] == player and not continuous):  # flip
    #             for coord in possibleFlip:
    #                 futureState[coord[0]][coord[1]] = player
    #             break