# Grid.py
import pygame
from random import randint
from Cube import Cube


class Grid:
    # This class contains all the code to handle the ENTIRE sudoku board
    def __init__(self, rows, cols, grid_generator, width, height, win, difficulty):
        self.rows = rows
        self.cols = cols
        self.model = None
        self.difficulty = difficulty
        self.grid_generator = grid_generator(rows, cols, difficulty)
        self.board = self.grid_generator.generate_new()
        self.solution = self.grid_generator.get_solution()
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.update_model()
        self.selected = None
        self.win = win

    def draw(self):
        # draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def generate_new_board(self, grid_gen, diff):
        # generate a new board
        self.difficulty = diff
        self.grid_generator = grid_gen(self.rows, self.cols, self.difficulty)
        self.board = self.grid_generator.generate_new()
        self.solution = self.grid_generator.get_solution()
        self.cubes = [[Cube(self.board[i][j], i, j, self.width, self.height) for j in range(self.cols)] for i in range(self.rows)]
        self.update_model()
        self.selected = None

    def place(self, val):
        # place val in selected square if it's empty
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if self.valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def hint_user(self):
        # pick a random empty square on the board and show the correct value
        while True:
            r = randint(0, 8)
            c = randint(0, 8)
            while self.board[r][c] != 0:
                r = randint(0, 8)
                c = randint(0, 8)

            self.select(r, c)
            self.cubes[r][c].set_hinted(True)
            if self.place(self.solution[r][c]):
                return True

        return False

    def sketch(self, val):
        # sketch/pencil in a value on the selected square
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def select(self, row, col):
        # reset all other selected cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        # remove the penciled in value at selected square
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        # determine the square a user clicked on
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        # determine if the board is finished
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        # function to determine if the board is solvable after placing a new value
        find = self.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        # solve the board and update the GUI to show solution's values
        self.update_model()
        find = self.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def show_solution(self, solution_win):
        # displays the entire solution for the current board
        sol_cubes = [[Cube(self.solution[i][j], i, j, self.width, self.height) for j in range(self.cols)] for i in range(self.rows)]

        # draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(solution_win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(solution_win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                sol_cubes[i][j].draw(solution_win)

    def find_empty(self, bo):
        # finds an empty square on board bo
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j)

        return None

    def get_difficulty(self):
        # return the current game's difficulty
        return self.difficulty

    def valid(self, bo, num, pos):
        # determine if a board is still valid if we were to add num at pos to bo
        # check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False
        # check col
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
