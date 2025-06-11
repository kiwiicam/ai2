import numpy as np
import random
import copy
from collections import deque

global epsilon

epsilon = 1
min_epsilon = 0.1
epsilon_decay = 0.95

class enviroment():
    def __init__(self):
        self.enviro = \
        [[-1, -1, -1, -1, -1, -1, -1],
         [-1, -90, -1, -90, -1, -90, -1],
         [-1, -90, -1, -90, -1, -90, -1],
         [-1, -90, -1, -1, -1, -1, -1],
         [-1, -90, -90, -90, -90, -90, +90]]

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.start_num = None
        self.generate_maze()


 
    def generate_maze(self):
        self.start_num = random.randint(0, self.rows - 1)
        start = (self.start_num, 0)
        goal = (random.randint(0, self.rows - 1), self.cols - 1)

        path = self.create_valid_path(start, goal)

        gx, gy = goal
        self.maze[gx][gy] = 90

        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in path and (i, j) != goal:
                    if random.random() < 0.96: #trap chance
                        self.maze[i][j] = -90

    def create_valid_path(self, start, goal):
        path = []
        visited = set()
        found = self._dfs(start, goal, visited, path)
        return path if found else self.create_valid_path(start, goal) 

    def _dfs(self, current, goal, visited, path):
        if current == goal:
            path.append(current)
            return True

        visited.add(current)
        x, y = current
        path.append(current)

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and (nx, ny) not in visited:
                if self._dfs((nx, ny), goal, visited, path):
                    return True

        path.pop()
        return False
    
def isTerminal(maze, location):
    move = location.split(",")
    if maze[int(move[0])][int(move[1])]-90 == 0 or maze[int(move[0])][int(move[1])]+90 == 0:
        return True
    else:
        return False

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

def actionIndex(action):
        index = None
        if action == "U":
            index = 0
        if action == "L":
            index = 1
        if action == "R":
            index = 2
        if action == "D":
            index = 3
        return index

def indexToAction(index):
    return ["U", "L", "R", "D"][index]

def calculateQScore(qtable, state, action, reward, next_state, terminal):
    discount_factor = 0.8
    learning_rate = 0.3
    action_index = actionIndex(action)
    current_q = qtable[state][action_index]
    max_future_q = np.max(qtable[next_state])
    new_q = current_q + learning_rate * (reward + discount_factor * max_future_q - current_q)
    #print(f"New Q value is {new_q}")
    return new_q

def mazeToState(stateArray, location):
    move = location.split(",")
    row = int(move[0])
    column = int(move[1])
    return stateArray[row][column]

def chooseAction(maze, location, epsilon, stateArray, qtable):
    moves = allLegalMoves(maze, location)
    state = mazeToState(stateArray, location)
    r = random.uniform(0, 1)
    if(r < epsilon):
        return random.choice(moves)
    else:
        qvalues = qtable[state]
        best_action_index = np.argmax(qvalues)
        best_action = indexToAction(best_action_index)
        while best_action not in moves:
            qvalues[best_action_index] = -999999
            best_action_index = np.argmax(qvalues)
            best_action = indexToAction(best_action_index)
        
        return best_action
    
def makeMove(action, location):
    move = location.split(",")
    row = int(move[0])
    column = int(move[1])
    if action == "U":
        row-=1
    if action == "L":
        column-=1
    if action == "R":
        column+=1
    if action == "D":
        row+=1
    return f"{row},{column}"

def train(training_count):
    row = random.randint(10, 25)
    column = random.randint(10, 25)
    mazeObj = MazeGenerator(row, column)
    maze = mazeObj.maze
    start_formatted = f"{mazeObj.start_num},0"
    location = start_formatted
    qtable = Qtable(row, column).qtable
    global epsilon
    for episode in range (training_count):
        location = start_formatted
        stateArr = createStateArray(maze).stateArray
        while True:
                state = mazeToState(stateArr, location)
                action = chooseAction(maze, location, epsilon, stateArr, qtable)
                location = makeMove(action, location)
                reward = calculateReward(maze, location)
                newState = mazeToState(stateArr, location)
                terminal = isTerminal(maze, location)
                action_index = actionIndex(action)
                qtable[state][action_index] = calculateQScore(qtable, state, action, reward, newState, terminal)
                epsilon =  max(min_epsilon, epsilon * epsilon_decay)
                if isTerminal(maze, location):
                    break
        if(episode % 100 == 0):
                print(f"episode {episode} out of {training_count}")      
    print("Training is finsihed")
    np.savetxt("maze.txt", maze)
    np.savetxt("qtable.txt", qtable, fmt="%.4f")
    with open("start.txt", "w") as f:
        f.write(start_formatted)

class createStateArray():
     
    def __init__(self, board):
        c=0
        self.stateArray = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
        for i in range(len(board)):
            for j in range(len(board[i])):
                self.stateArray[i][j] = c
                c+=1


class Qtable():
    def __init__(self, row, col):
        self.qtable = np.zeros((row * col, 4))

def displayPath(maze, locations):
    mazeRoute = copy.deepcopy(maze)
    for location in locations:
        move = location.split(",")
        mazeRoute[int(move[0])][int(move[1])] = "x"
    printMazePath(mazeRoute)

def printMazePath(maze):
    print("")
    for row in maze:
        formatted_row = ""
        for cell in row:
            if isinstance(cell, str):
                formatted_row += f"{cell:^6}"  # center align
            else:
                formatted_row += f"{cell:^6.1f}"  # one decimal place
        print(formatted_row)
    print("")
    



def solveMaze():
    qtable = np.loadtxt('qtable.txt')
    maze = np.loadtxt('maze.txt').tolist()
    printMazePath(maze)
    location = None
    with open("start.txt", "r") as f:
        location = f.read().strip()
    print(f"Starting location is {location}")
    stateArr = createStateArray(maze).stateArray
    locationArr = []
    print("The best route goes: ")
    while True:
        locationArr.append(location)
        print(f"{location}", end=" ")
        print("->", end=" ")
        state = mazeToState(stateArr, location)
        qvalues = qtable[state]
        legal_moves = allLegalMoves(maze, location)
        legal_moves_indexes = [actionIndex(move) for move in legal_moves]
        best_move_index = np.argmax(qvalues)
        if best_move_index not in legal_moves_indexes:
            print("ILLEGAL MOVE SOMEHOW????")
        best_move = indexToAction(best_move_index)
        location = makeMove(best_move, location)
        if isTerminal(maze, location):
            print(f"{location} (end)")
            locationArr.append(location)
            displayPath(maze, locationArr)
            break
    
train(10000)
solveMaze()
while True:
    hi = 5

