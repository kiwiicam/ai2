from Minimax import get_best_move

class Board:
    def __init__(self):
        self.board = [[0, 0, 0], 
                      [0, 0, 0], 
                      [0, 0, 0]]
    
    def checkWin(self, player):
        return (
            # Rows
            (self.board[0][0] == self.board[0][1] == self.board[0][2] == player)
            or (self.board[1][0] == self.board[1][1] == self.board[1][2] == player)
            or (self.board[2][0] == self.board[2][1] == self.board[2][2] == player)
            or
            # Columns
            (self.board[0][0] == self.board[1][0] == self.board[2][0] == player)
            or (self.board[0][1] == self.board[1][1] == self.board[2][1] == player)
            or (self.board[0][2] == self.board[1][2] == self.board[2][2] == player)
            or
            # Diagonals
            (self.board[0][0] == self.board[1][1] == self.board[2][2] == player)
            or (self.board[0][2] == self.board[1][1] == self.board[2][0] == player)
        )
    def calculateReward(self, player):
        if self.checkWin(player):
            return 1  # Player wins
        elif self.checkWin(3 - player):
            return -1
        elif self.checkDraw():
            return 0.2
        else:
            return -0.01
    
    def checkDraw(self):
        return not(
            self.board[0][0] == 0 or self.board[0][1] == 0 or
            self.board[0][2] == 0 or self.board[1][0] == 0 or
            self.board[1][1] == 0 or self.board[1][2] == 0 or
            self.board[2][0] == 0 or self.board[2][1] == 0 or
            self.board[2][2] == 0
        )
    def allLegalMoves(self):
        legal_moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    legal_moves.append(f"{row},{col}")
        return legal_moves



    def makeMove(self, move, player):
        #check if move is legal first:
        index_to_action_map = {
    0: "0,0", 1: "0,1", 2: "0,2",
    3: "1,0", 4: "1,1", 5: "1,2",
    6: "2,0", 7: "2,1", 8: "2,2"
}
        try:
            move = index_to_action_map[move]
            move = move.split(",")
        except:
            move = move.split(",")
        #print(f"the move is {move} by player: {player}")
        if int(move[0]) <= 2 and int(move[1]) <= 2:
            if self.board[int(move[0])][int(move[1])] == 0:
                self.board[int(move[0])][int(move[1])] = player
                return True
        return False

    def printBoard(self):
        print(self.board[0])
        print(self.board[1])
        print(self.board[2])

def gameLoop():
    board = Board()
    while True:
        board.printBoard()
        while True:
            move = input("PLAYER 1 Enter your move like this x,x: ")
            if board.makeMove(move, 1):
                break
        if board.checkWin(1) == True:
            board.printBoard() 
            return "Player 1 wins!"
        if board.checkDraw():
            board.printBoard() 
            return "THE GAME IS A DRAW"   
        board.printBoard()
        while True:

            bot_move = get_best_move(board.board)
            if board.makeMove(bot_move, 2):
                break
        if board.checkWin(2) == True:
            board.printBoard() 
            return "Player 2 wins!"
        if board.checkDraw():
            board.printBoard() 
            return "THE GAME IS A DRAW" 

#gameLoop()