import numpy as np
from tictactoe import Board 
from tictactoe import gameLoop
from Minimax import get_best_move
from Minimax import check_two_in_a_row
import os
import random

class createQtable():
    num_states = 3 ** 9
    num_actions = 9
    q_table = np.random.uniform(-0.01, 0.01, (num_states, num_actions))

def board_to_state(board):
    state = 0
    for i in range(3):
        for j in range(3):
            state = state * 3 + board[i][j]
    return state

epsilon = 1
epsilon_min = 0.01
epsilon_decay = 0.99999

action_to_index_map = {
    "0,0": 0, "0,1": 1, "0,2": 2,
    "1,0": 3, "1,1": 4, "1,2": 5,
    "2,0": 6, "2,1": 7, "2,2": 8
}

def choose_action(state, q_table, epsilon, board):
    legal_actions_str_arr = board.allLegalMoves()

    legal_actions = [action_to_index_map[a] for a in legal_actions_str_arr]

    if not legal_actions:
        print("No legal moves available! The game is over.")
        return None
    
    r = random.uniform(0, 1)
    
    if r < epsilon:
        action = random.choice(legal_actions)
    else:
        q_values = q_table[state]
        best_action = np.argmax(q_values)

        while best_action not in legal_actions:
            q_values[best_action] = -999999
            best_action = np.argmax(q_values)
        
        action = best_action 
    

    return action




def apply_action(board, move, player):
    board.makeMove(move, player)    


def calculate_reward(board, player):
    if board.checkWin(player): return 10
    if board.checkWin(3-player): return -10
    if board.checkDraw(): return 3 
    center_bonus = 0.5 if board.board[1][1] == player else -0.3
    two_in_row = 1.5 if check_two_in_a_row(board.board, player) else 0
    return 0.1 + center_bonus + two_in_row


learning_rate = 0.25

discount_factor = 0.9

def calculateQscore(q_table, state, action, reward, next_state, terminal):
    current_q = q_table[state][action]
    max_future_q = 0 if terminal else np.max(q_table[next_state])
    new_q = current_q + learning_rate * (reward + discount_factor * max_future_q - current_q)
    #print(f"updating Q table to {new_q}")
    q_table[state][action] = new_q
    


def train(num_episodes, existing):
    global epsilon
    if existing and os.path.exists('q_table.npy'):
        q_table = np.load('q_table.npy')
    else:
        q_table = createQtable().q_table

    for episode in range(num_episodes):
        board = Board()
        prev_state = None
        prev_action = None
        
        while True:
            # Q-bot's move (Player 1)
            state = board_to_state(board.board)
            action = choose_action(state, q_table, epsilon, board)
            if action is None: break
            
            apply_action(board, action, 1)
            
            # Calculate reward after Q-bot's move
            reward = calculate_reward(board, 1)
            terminal = board.checkWin(1) or board.checkDraw()
            next_state = None if terminal else board_to_state(board.board)
            
            # Store previous state/action before opponent moves
            prev_state = state
            prev_action = action
            
            calculateQscore(q_table, state, action, reward, next_state, terminal)
            if terminal: break

            # Minimax's move (Player 2)
            if random.random() < 0.3:  # 30% chance of weaker opponent
                best_move = get_best_move(board.board, depth=1)
            else:
                best_move = get_best_move(board.board)
            board.makeMove(best_move, 2)
            
            # Update Q-table based on opponent's move
            if board.checkWin(2):
                reward = -10  # Q-bot loses
                terminal = True
                calculateQscore(q_table, prev_state, prev_action, reward, None, terminal)
                break
            elif board.checkDraw():
                reward = 0.5
                terminal = True
                calculateQscore(q_table, prev_state, prev_action, reward, None, terminal)
                break

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        if episode % 1000 == 0:
            print(f"Episode {episode}, Epsilon: {epsilon:.3f}")

    np.save('q_table.npy', q_table)

def verseBot():
    board = Board()
    q_array = np.load('q_table.npy')
    print(q_array)
    while True:
        board.printBoard()
        playermove = input("Enter your move in the format x,x")
        board.makeMove(playermove, 1)
        if board.checkWin(1) or board.checkDraw():
            print("GAME OVER OR DRAW")
            break
    #get numpy var in from text that its been saved too
        board.printBoard()
        state = board_to_state(board.board)
    #get state for current game state using board_to_state()
        movelist = q_array[state]  # all Q-values for this state (length 9)
        legal_moves = board.allLegalMoves()  # e.g. ["0,0", "1,2", "2,1"]
        legal_indices = [action_to_index_map[move] for move in legal_moves]  # e.g. [0, 5, 7]
        # Now get Q-values only for legal moves
        legal_q_values = movelist[legal_indices]
        best_legal_q_index = np.argmax(legal_q_values)
        best_move = legal_indices[best_legal_q_index] 
        print(f"The bot's best move is: {best_move}")
        board.makeMove(best_move, 2)
        if board.checkWin(2) or board.checkDraw():
            print("GAME OVER OR DRAW")
            break      
    #and then use max() to find the move with the highest q value
#train(100000, True)
verseBot()
