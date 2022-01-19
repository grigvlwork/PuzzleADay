def rotate_matrix_right(a):
    rows = len(a)
    cols = len(a[0])
    b = [[0] * rows for i in range(cols)]
    for i in range(rows):
        for j in range(cols):
            b[j][rows - i - 1] = a[i][j]
    return b


def rotate_matrix_left(a):
    rows = len(a)
    cols = len(a[0])
    b = [[0] * rows for i in range(cols)]
    for i in range(rows):
        for j in range(cols):
            b[cols - j - 1][i] = a[i][j]
    return b


def mirror_matrix(a):
    rows = len(a)
    cols = len(a[0])
    b = [[0] * cols for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            b[rows - i - 1][j] = a[i][j]
    return b
