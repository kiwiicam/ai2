def checkWin(board, player):
    return (
        # Rows
        (board[0][0] == board[0][1] == board[0][2] == player) or
        (board[1][0] == board[1][1] == board[1][2] == player) or
        (board[2][0] == board[2][1] == board[2][2] == player) or
        # Columns
        (board[0][0] == board[1][0] == board[2][0] == player) or
        (board[0][1] == board[1][1] == board[2][1] == player) or
        (board[0][2] == board[1][2] == board[2][2] == player) or
        # Diagonals
        (board[0][0] == board[1][1] == board[2][2] == player) or
        (board[0][2] == board[1][1] == board[2][0] == player)
    )

def checkDraw(board):
    return all(cell != 0 for row in board for cell in row) and \
           not checkWin(board, 1) and not checkWin(board, 2)

def makeMove(board, move, player):
    row, col = map(int, move.split(','))
    if board[row][col] == 0:
        new_board = [row[:] for row in board]  # Create copy
        new_board[row][col] = player
        return new_board
    return None  # Invalid move

def check_two_in_a_row(board, player):
    # Check rows
    for row in range(3):
        if (board[row][0] == board[row][1] == player and board[row][2] == 0) or \
           (board[row][0] == board[row][2] == player and board[row][1] == 0) or \
           (board[row][1] == board[row][2] == player and board[row][0] == 0):
            return True
    
    # Check columns
    for col in range(3):
        if (board[0][col] == board[1][col] == player and board[2][col] == 0) or \
           (board[0][col] == board[2][col] == player and board[1][col] == 0) or \
           (board[1][col] == board[2][col] == player and board[0][col] == 0):
            return True
    
    # Check diagonals
    if (board[0][0] == board[1][1] == player and board[2][2] == 0) or \
       (board[0][0] == board[2][2] == player and board[1][1] == 0) or \
       (board[1][1] == board[2][2] == player and board[0][0] == 0):
        return True
    
    if (board[0][2] == board[1][1] == player and board[2][0] == 0) or \
       (board[0][2] == board[2][0] == player and board[1][1] == 0) or \
       (board[1][1] == board[2][0] == player and board[0][2] == 0):
        return True
    
    return False

def allLegalMoves(board):
    return [f"{row},{col}" for row in range(3) for col in range(3) if board[row][col] == 0]

def evaluate(board):
    if checkWin(board, 2): return +10
    if checkWin(board, 1): return -10
    if checkDraw(board): return 0.1
    if check_two_in_a_row(board, 2): return +5
    if check_two_in_a_row(board, 1): return -5
    return 0

def minimax(board, depth, is_maximizing):
    if checkWin(board, 2): return 10
    if checkWin(board, 1): return -10
    if checkDraw(board): return 0.1
    if depth == 0: return evaluate(board)

    legal_moves = allLegalMoves(board)
    if is_maximizing:
        best_score = -float('inf')
        for move in legal_moves:
            new_board = makeMove(board, move, 2)
            if new_board:  # If move is valid
                score = minimax(new_board, depth-1, False)
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in legal_moves:
            new_board = makeMove(board, move, 1)
            if new_board:  # If move is valid
                score = minimax(new_board, depth-1, True)
                best_score = min(score, best_score)
        return best_score

def get_best_move(board, depth=2):
    legal_moves = allLegalMoves(board)
    best_score = -float('inf')
    best_move = None
    for move in legal_moves:
        new_board = makeMove(board, move, 2)
        if new_board:  # If move is valid
            score = minimax(new_board, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move