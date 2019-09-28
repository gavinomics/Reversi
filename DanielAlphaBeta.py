import math
import copy
import pdb
from ModifiedAlphaBeta import modifiedAlphaBetaSearch

myPlayerNumber = 0
otherPlayer = 0
currentRound = 0 #NEED THIS?
gamePlay = "start"
ALPHA_BETA_DEPTH = 3
EXPLORE_DEPTH = 2

def danielAlphaBetaSearch(depth, state, player, round):
    global myPlayerNumber
    global currentRound
    global otherPlayer
    myPlayerNumber = player
    otherPlayer = 1 if player == 2 else 2
    currentRound = round

    _, action = exploreTree(state, 1, gamePlay)

    return action

def exploreTree(state, depth, path):
    if (depth == 0 or len(getValidFutureMoves(state, myPlayerNumber)) == 0):
        return getUtility(state), None
    bestScore = 0
    bestMove = None;
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(8):
        print(state[7-i])
    print(getValidFutureMoves(state, myPlayerNumber))
    for a in getValidFutureMoves(state, myPlayerNumber):
        path += f" {myPlayerNumber}:{a[0]},{a[1]}"
        futureState = getResults(state, a, myPlayerNumber)
        action = modifiedAlphaBetaSearch(ALPHA_BETA_DEPTH, futureState, otherPlayer)
        print(f"If i move {a}, theyll move {action}")
        path += f" {otherPlayer}:{action[0]},{action[1]}"
        score, move = exploreTree(getResults(futureState, action, otherPlayer), depth-1, path)
        if (score > bestScore): 
            bestScore = score
            bestMove = a
    return bestScore, bestMove



def maxValue(depth, state, alpha, beta):
    print("Enter maxValue func")
    print("Depth: ", depth)

    action = None
    utility = -math.inf

    if depth == 0 or len(getValidFutureMoves(state, myPlayerNumber)) == 0:
        utility = getUtility(state)
        return utility, action

    # if len(getValidFutureMoves(state, myPlayerNumber)) == 0:
    #     print("Valid moves is Empty!!!")

    for a in getValidFutureMoves(state, myPlayerNumber):

        actionUtilityofMinimizer, _ = minValue(depth-1, getResults(state, a, myPlayerNumber), alpha, beta)

        if actionUtilityofMinimizer > utility:
            print(actionUtilityofMinimizer, " is greater than ", utility)
            utility = actionUtilityofMinimizer
            action = a

        if utility >= beta:
            print("Prune")
            return utility, action

        alpha = max(alpha, utility)
        print("Alpha after comparison: ", alpha)

    if action == None:
        print("************ ACTION IS NONE!!!!!!***************")

    return utility, action


def minValue(depth, state, alpha, beta):
    print("Enter minValue func")
    print("Depth: ", depth)
    action = None
    utility = math.inf
    playerNum = 1 if myPlayerNumber == 2 else 1

    if depth == 0 or len(getValidFutureMoves(state, playerNum)) == 0:
        utility = getUtility(state)
        return utility, action

    for a in getValidFutureMoves(state, playerNum):

        actionUtilityofMaximizer, _ = maxValue(depth-1, getResults(state, a, playerNum), alpha, beta)

        if actionUtilityofMaximizer < utility:
            print(actionUtilityofMaximizer, " is less than ", utility)
            utility = actionUtilityofMaximizer
            action = a

        if utility <= beta:
            print("Prune")
            return utility, action

        beta = min(beta, utility)
        print("Beta after comparison: ", alpha)

    if action == None:
        print("************ ACTION IS NONE!!!!!!***************")

    return utility, action

def getResults(state, action, player):

    futureState = copy.deepcopy(state)

    # futureState = state

    futureState[action[0]][action[1]] = player

    flipThePieces(futureState, action, player, 1, 1)
    flipThePieces(futureState, action, player, 0, 1)
    flipThePieces(futureState, action, player, -1, 1)
    flipThePieces(futureState, action, player, 1, 0)
    flipThePieces(futureState, action, player, -1, 0)
    flipThePieces(futureState, action, player, -1, -1)
    flipThePieces(futureState, action, player, 0, -1)
    flipThePieces(futureState, action, player, 1, -1)

    print("\n")
    print("Player: ", player)
    print("Action: ", action)

    for x in range(8):
        print(futureState[7-x])
    return futureState

def flipThePieces(futureState, move, player, moveRow, moveColumn):
    row = move[0]
    column = move[1]
    continuous = True
    possibleFlip = []
    while(True):
        row += moveRow
        column += moveColumn
        if (row > 7 or row < 0 or column > 7 or column <0):
            break
        elif (futureState[row][column] == 0):
            break
        elif (futureState[row][column] == player and continuous):
            break
        elif (futureState[row][column] != player):
            continuous = False
            possibleFlip.append([row, column])
        elif (futureState[row][column] == player and not continuous): #flip
            for coord in possibleFlip:
                futureState[coord[0]][coord[1]] = player
            break


def getValidFutureMoves(futureState, me):
    validMoves = []
    for i in range(8):
        for j in range(8):
            if (futureState[i][j] == 0):
                if (couldBe(futureState, i, j, me)):
                    validMoves.append([i, j])
    return validMoves

def getUtility(state):
    score = 0;
    for i in range(8):
        for j in range(8):
            if (state[i][j] == myPlayerNumber):
                score += 1
    return score

def couldBe(futureState, row, col, me):
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            if ((incx == 0) and (incy == 0)):
                continue

            if (checkDirection(futureState, row, col, incx, incy, me)):
                return True

    return False

def checkDirection(futureState, row, col, incx, incy, me):
    sequence = []
    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        sequence.append(futureState[r][c])

    count = 0

    for i in range(len(sequence)):
        if (me == 1):
            if (sequence[i] == 2):
                count = count + 1
            else:
                if ((sequence[i] == 1) and (count > 0)):
                    return True
                break
        else:
            if (sequence[i] == 1):
                count = count + 1
            else:
                if ((sequence[i] == 2) and (count > 0)):
                    return True
                break

    return False

