import numpy as np
import random
class enviroment():
    def __init__(self):
        self.enviro = \
        [[-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -9, -9, -1, -1, -1],
         [-1, -1, -9, -9, -1, -9, -1],
         [-1, -1, -1, -1, -1, -9, -1],
         [-1, -9, -9, -9, -9, -9, +9]]
        
def isTerminal(maze):
    maze

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

def mazeToState(stateArray, location):
    move = location.split(",")
    row = int(move[0])
    column = int(move[1])
    return stateArray[row][column]

def chooseAction(maze, epsilon):
    r = random.uniform(0, 1)
class createStateArray():
    
    def __init__(self, board):
        c=0
        self.stateArray = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.stateArray[i][j] = c
                c+=1


class Qtable():
    def __init__(self):
        self.qtable = np.zeros((35,4))


