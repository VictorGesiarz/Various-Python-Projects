import random
import Rules


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def easy_bot(b):
    options = []
    for i in range(3):
        for j in range(3):
            if b.board[i][j] == "-":
                options.append((i, j))
    option = random.randint(0, len(options)-1)
    b.board[options[option][0]][options[option][1]] = b.pieces[b.moves % 2]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

max_min = []


def find_best_move(b):
    moves = find_moves(b.board)
    evaluations = []
    depth = 9 - b.moves
    for move in moves:
        copy = copy_matrix(b.board)
        copy[move[0]][move[1]] = max_min[0]
        evaluations.append(minimax(copy, depth, False))
    max_evaluation = max(evaluations)
    index = evaluations.index(max_evaluation)
    return moves[index]


def minimax(board, depth, maximizing_player):
    win = Rules.check_win(board)
    if depth == 1 or win:
        if maximizing_player and win:
            return -1
        elif not maximizing_player and win:
            return 1
        else:
            return 0

    if maximizing_player:
        turn = max_min[0]
        max_evaluation = -10
        moves = find_moves(board)
        for move in moves:
            copy = copy_matrix(board)
            copy[move[0]][move[1]] = turn
            evaluation = minimax(copy, depth - 1, False)
            max_evaluation = max(max_evaluation, evaluation)
        return max_evaluation

    else:
        turn = max_min[1]
        min_evaluation = 10
        moves = find_moves(board)
        for move in moves:
            copy = copy_matrix(board)
            copy[move[0]][move[1]] = turn
            evaluation = minimax(copy, depth - 1, True)
            min_evaluation = min(min_evaluation, evaluation)
        return min_evaluation


def find_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                move = (i, j)
                moves.append(move)
    return moves


def copy_matrix(board):
    copy = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(board[i][j])
        copy.append(row)
    return copy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
