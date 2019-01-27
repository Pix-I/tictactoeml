class Oxo_board:
    def __init__(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.goodMove = 1
        self.badMove = -2
        self.veryBadMove = -3

    def place_cross(self, x, y):
        x = x - 1
        y = y - 1
        if self.board[x][y] == ' ':
            self.board[x][y] = 'X'
            return self.goodMove
        elif self.board[x][y] == 'X':
            return self.badMove
        elif self.board[x][y] == 'O':
            return self.veryBadMove
        return self.veryBadMove

    def place_bubble(self, x, y):
        x = x - 1
        y = y - 1
        if self.board[x][y] == ' ':
            self.board[x][y] = 'O'
            return self.goodMove
        elif self.board[x][y] == 'O':
            return self.badMove
        elif self.board[x][y] == 'X':
            return self.veryBadMove
        return self.veryBadMove

    def check_diagonal_oxo(self):
        if self.board[1][1] == 'O':
            return self.checkDiagonalOOO()
        if self.board[1][1] == 'X':
            return self.checkDiagonalXXX()

        return False

    def check_horizontal_oxo(self):
        for row in self.board:
            if row == ['O', 'O', 'O'] or row == ['X','X','X']:
                return True
        return False

    def check_vertical_oxo(self):
        for x in range(3):
            if [self.board[0][x], self.board[1][x], self.board[2][x]] == ['O', '0', 'O']:
                return True
            if [self.board[0][x], self.board[1][x], self.board[2][x]] == ['x', 'X', 'X']:
                return True
        return False

    def check_oxo(self):
        if self.check_diagonal_oxo():
            return True
        if self.check_horizontal_oxo():
            return True
        if self.check_vertical_oxo():
            return True
        return False

    def has_move(self):
        for row in self.board:
            for c in row:
                if c == ' ':
                    return True
        return False

    def reset(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def printBoard(self):
        for row in self.board:
            print(row)

    def get_hash(self):
        stra = 'hash'
        for row in self.board:
            stra = stra + ''.join(row)
        return stra

    def checkDiagonalXXX(self):
        if self.board[0][0] == 'X' and self.board[2][2] == 'X':
            return True
        if self.board[2][0] == 'X' and self.board[0][2] == 'X':
            return True
        return False
    def checkDiagonalOOO(self):
        if self.board[0][0] == 'O' and self.board[2][2] == 'O':
            return True
        if self.board[2][0] == 'O' and self.board[0][2] == 'O':
            return True
        return False