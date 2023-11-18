# GridGenerator.py
from random import randint, shuffle


class GridGenerator:
    # this class generates new, unique grids
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    counter = 1

    def __init__(self, rows, cols, difficulty):
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty
        self.solution = []

    def solve(self, board):
        # find open spot on grid
        find = self.find_open(board)
        if not find:
            return True
        else:
            row, col = find
        # try to find valid number to place on grid
        for i in range(1, 10):
            if valid(board, i, (row, col)):
                board[row][col] = i

                # check if grid is full
                if self.check_grid(board):
                    self.set_counter(self.counter + 1)
                else:
                    # check if board can be solved
                    if self.solve(board):
                        return True

                board[row][col] = 0

        return False

    def fill_board(self):
        find = self.find_open(self.grid)
        if not find:
            return True
        else:
            row, col = find

        shuffle(numberList)
        for value in numberList:
            if valid(self.grid, value, (row, col)):
                self.grid[row][col] = value

                if self.check_grid(self.grid):
                    return True
                else:
                    if self.fill_board():
                        return True

                self.grid[row][col] = 0

        return False

    def generate_new(self):
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.fill_board()
        self.set_solution(self.grid)

        attempts = self.difficulty
        while attempts > 0:
            # select random cell that isn't empty
            row = randint(0, 8)
            col = randint(0, 8)
            while self.grid[row][col] == 0:
                row = randint(0, 8)
                col = randint(0, 8)

            backup = self.grid[row][col]
            self.grid[row][col] = 0

            copy = []
            for i in range(0, 9):
                copy.append([])
                for j in range(0, 9):
                    copy[i].append(self.grid[i][j])

            self.set_counter(0)
            self.solve(copy)
            if self.counter != 1:
                self.grid[row][col] = backup
                attempts -= 1

        return self.grid

    def find_open(self, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == 0:
                    return (i, j)

        return None

    def check_grid(self, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == 0:
                    return False

        return True

    def print_grid(self):
        for i in range(self.rows):
            print(str(self.grid[i]))

        print("\n\n")

    def print_solution(self):
        for i in range(self.rows):
            print(str(self.solution[i]))

        print("\n\n")

    def get_solution(self):
        return self.solution

    def set_counter(self, value):
        self.counter = value

    def set_solution(self, board):
        s = []
        for i in range(self.rows):
            s.append([])
            for j in range(self.cols):
                s[i].append(board[i][j])

        self.solution = s


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]


