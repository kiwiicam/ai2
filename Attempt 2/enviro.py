import numpy as np

class enviroment():
    def __init__(self):
        self.enviro = \
        [[-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -9, -9, -1, -1, -1],
         [-1, -1, -9, -9, -1, -9, -1],
         [-1, -1, -1, -1, -1, -9, -1],
         [-1, -9, -9, -9, -9, -9, +9]]
        
def isTerminal(board):
    board

def allLegalMoves(maze, location):
    move = location.split(",")
    moveRow = int(move[0])
    moveHorizontal = int(move[1])

    height = len(maze)
    length = len(maze[0])

    movelist = []
    if moveRow != 0:
        movelist.append("U")
    if moveHorizontal !=0:
        movelist.append("L")
    if moveHorizontal < length-1:
        movelist.append("R")
    if moveRow < height-1:
        movelist.append("D")
    return movelist

def calculateReward(maze, location):
    move = location.split(",")
    return maze[int(move[0])][int(move[1])]

def calculateQScore(qtable):
    discount_factor = 1
    learning_rate = 1

def mazeToState(board):
    board
    
class Qtable():
    def __init__(self):
        self.qtable = np.zeros((35,4))

