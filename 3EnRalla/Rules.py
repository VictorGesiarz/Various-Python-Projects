def check_win(matrix):
    col_matrix, diagonals = transform_matrix(matrix)
    for i in range(3):
        if len(set(matrix[i])) == 1 and set(matrix[i]) != {'-'}:
            return (i, 0), (i, 1), (i, 2)
        elif len(set(col_matrix[i])) == 1 and set(col_matrix[i]) != {'-'}:
            return (0, i), (1, i), (2, i)

    if len(set(diagonals[0])) == 1 and set(diagonals[0]) != {'-'}:
        return (0, 0), (1, 1), (2, 2)
    elif len(set(diagonals[1])) == 1 and set(diagonals[1]) != {'-'}:
        return (0, 2), (1, 1), (2, 0)


def transform_matrix(board):
    m = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            row.append(board[j][i])
        m.append(row)

    d1 = []
    d2 = []
    for i in range(len(board)):
        d1.append(board[i][i])
        d2.append(board[i][len(board)-1-i])
    return m, [d1, d2]
