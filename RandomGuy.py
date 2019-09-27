import sys
import pdb;
import copy
import socket
import time
from random import randint
from ReversiRandom_Python.MinimaxCode import minimax
from ReversiRandom_Python.maximin import maximin

t1 = 0.0  # the amount of time remaining to player 1
t2 = 0.0  # the amount of time remaining to player 2

state = [[0 for x in range(8)] for y in range(8)]  # state[0][0] is the bottom left corner of the board (on the GUI)
myNumber = 0; #assigned when game starts, 1 or 2
treeIndex = {}
currentRound = 0

# You should modify this function
# validMoves is a list of valid locations that you could place your "stone" on this turn
# Note that "state" is a global variable 2D list that shows the state of the game
def move(validMoves):
    # just return a random move

    # mm = minimax(depth=3, nodeIndex=0, maximizingPlayer=2, values=, alpha=, beta):)
    mm = maximin()

    validMove = mm.alphaBetaSearch(state)

    print("VALID MOVES: \n", validMoves)
    myMove = validMoves[0][0]
    if (currentRound < 5):
        myMove = randint(0, len(validMoves) - 1)
    else:
        score, bestMove = recursiveStateMaker(state, 5, myNumber, "root")
        myMove = validMoves.index(bestMove)
    return myMove


def recursiveStateMaker(currentState, depth, player, parentAddress):
    if (depth == 0): 
        value = getScore(currentState) #this variable just for printing
        print(f"Score: {value}")
        return getScore(currentState), None
    moves = getValidFutureMoves(currentState, player)
    scores = []
    moveDict = {}
    for move in moves:
        nextState = createFutureState(currentState, move, player)
        nextPlayer = 2 if player == 1 else 1
        nextAddress = f"{parentAddress}---Player{player}:({move[0]},{move[1]})"
        print(nextAddress)
        for i in range(8):
            print(nextState[7-i])
        score, _ = recursiveStateMaker(nextState, depth-1, nextPlayer, nextAddress)
        if (moveDict.get(score) == None):
            moveDict[score] = move

        scores.append(score)
        if (treeIndex.get(parentAddress) != None):
            if (player != myNumber):
                if (score > treeIndex[parentAddress]):
                    print("prune")
                    break
            else:
                if (score < treeIndex[parentAddress]):
                    print("prune")
                    break
    if (len(scores)==0): return -100, None #What happens when no moves left? How to score?
    result = max(scores) if (player == myNumber) else min(scores)
    treeIndex[parentAddress] = result
    return result, moveDict[result]


def createFutureState(state, move, player):
    futureState = copy.deepcopy(state)
    futureState[move[0]][move[1]] = player
    flipThePieces(futureState, move, player, 1, 0)
    flipThePieces(futureState, move, player, 1, 1)
    flipThePieces(futureState, move, player, 0, 1)
    flipThePieces(futureState, move, player, -1, 1)
    flipThePieces(futureState, move, player, -1, 0)
    flipThePieces(futureState, move, player, -1, -1)
    flipThePieces(futureState, move, player, 0, -1)
    flipThePieces(futureState, move, player, 1, -1)
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
                if (couldBe(i, j, me)):
                    validMoves.append([i, j])
    return validMoves

def getScore(state):
    score = 0;
    for i in range(8):
        for j in range(8):
            if (state[i][j] == myNumber):
                score += 1
    return score

# establishes a connection with the server
def initClient(me, thehost):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (thehost, 3333 + me)
    print('starting up on %s port %s' % server_address, file=sys.stderr)
    sock.connect(server_address)

    info = sock.recv(1024)

    print(info)

    return sock


# reads messages from the server
def readMessage(sock):
    message = sock.recv(1024).decode("utf-8").split("\n")
    # print(message)

    turn = int(message[0])
    print("Turn: " + str(turn))

    if (turn == -999):
        time.sleep(1)
        sys.exit()

    round = int(message[1])
    print("Round: " + str(round))
    global currentRound
    currentRound = round
    print(currentRound)
    # t1 = float(message[2])  # update of the amount of time available to player 1
    # print t1
    # t2 = float(message[3])  # update of the amount of time available to player 2
    # print t2

    count = 4

    for i in range(8):
        for j in range(8):
            state[i][j] = int(message[count])
            count = count + 1
        print(state[i])

    return turn, round


def checkDirection(row, col, incx, incy, me):
    sequence = []
    for i in range(1, 8):
        r = row + incy * i
        c = col + incx * i

        if ((r < 0) or (r > 7) or (c < 0) or (c > 7)):
            break

        sequence.append(state[r][c])

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


def couldBe(row, col, me):
    for incx in range(-1, 2):
        for incy in range(-1, 2):
            if ((incx == 0) and (incy == 0)):
                continue

            if (checkDirection(row, col, incx, incy, me)):
                return True

    return False


# generates the set of valid moves for the player; returns a list of valid moves (validMoves)
def getValidMoves(round, me):
    validMoves = []
    print("Round: " + str(round))

    for i in range(8):
        print(state[i])

    if (round < 4):
        if (state[3][3] == 0):
            validMoves.append([3, 3])
        if (state[3][4] == 0):
            validMoves.append([3, 4])
        if (state[4][3] == 0):
            validMoves.append([4, 3])
        if (state[4][4] == 0):
            validMoves.append([4, 4])
    else:
        for i in range(8):
            for j in range(8):
                if (state[i][j] == 0):
                    if (couldBe(i, j, me)):
                        validMoves.append([i, j])

    return validMoves


# main function that (1) establishes a connection with the server, and then plays whenever it is this player's turn
# noinspection PyTypeChecker
def playGame(me, thehost):
    # create a random number generator

    sock = initClient(me, thehost)

    while (True):
        print("Your Turn")
        status = readMessage(sock)

        if (status[0] == me):
            print("Move")
            validMoves = getValidMoves(status[1], me)
            print(validMoves)
            myMove = move(validMoves)

            sel = str(validMoves[myMove][0]) + "\n" + str(validMoves[myMove][1]) + "\n"
            print("<" + sel + ">")
            sock.send(sel.encode("utf-8"))
            print("sent the message")
        else:
            print("Waiting for other player...")


# call: python RandomGuy.py [ipaddress] [player_number]
# ipaddress is the ipaddress on the computer the server was launched on.  Enter "localhost" if it is on the same computer
# player_number is 1 (for the black player) and 2 (for the white player)
if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    print(str(sys.argv[1]))
    myNumber = int(sys.argv[2])
    playGame(int(sys.argv[2]), sys.argv[1])