# GUI.py
import pygame
import time
from Grid import Grid
from GridGenerator import GridGenerator
pygame.font.init()


def game_won(win, board, t, strikes, options, difficulty, hints_remaining):
    # this function calls the redraw_window function then displays the game over text

    fnt = pygame.font.SysFont("comicsans", 40)
    game_over_text = fnt.render("Game Over! You Win!", 1, (0, 255, 0))

    f = pygame.Surface((540, 540))
    f.fill((140, 140, 140))
    f.set_alpha(150)
    redraw_window(win, board, t, strikes, options, difficulty, hints_remaining)
    win.blit(f, (0, 0))
    win.blit(game_over_text, (100, 250))
    pygame.display.update()


def show_solution(win, board):
    # function to show the board's solution to the user once 'Show solution' menu button is pressed
    solution_win = pygame.Surface((540, 540))
    solution_win.fill((255, 255, 255))

    board.show_solution(solution_win)
    win.blit(solution_win, (0, 0))
    pygame.display.update()


def redraw_window(win, board, t, strikes, options, difficulty, hints_remaining):
    # function to redraw the entire pygame window to the user
    win.fill((255, 255, 255))
    # draw time
    fnt = pygame.font.SysFont("comicsans", 25)
    text = fnt.render("Time: " + format_time(t), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # draw strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # draw options
    for text, rect, color in options:
        pygame.draw.rect(win, color, rect)
        win.blit(text, rect)

    # difficulty label
    fnt2 = pygame.font.SysFont("comicsans", 20)
    diff_text = fnt2.render("Difficulty", 1, (0, 0, 0))
    win.blit(diff_text, (570, 170))
    # draw difficulty
    for text, rect, color in difficulty:
        pygame.draw.rect(win, color, rect)
        win.blit(text, rect)

    # draw hints remaining
    fnt3 = pygame.font.SysFont("comicsans", 15)
    text = fnt3.render("Hints remaining: " + str(hints_remaining), 1, (0, 0, 0))
    win.blit(text, (560, 560))
    # draw grid and board
    board.draw()


def format_time(secs):
    # function to format the time in seconds to minute:second format
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def highlight_diff(difficulty, cur_diff):
    # function to set the color of the current difficulty level to be highlighted
    for diff in difficulty:
        if diff == cur_diff:
            diff[2] = (185, 190, 195)
        else:
            diff[2] = (255, 255, 255)


def setup_difficulty():
    # function to setup difficulty buttons
    fnt = pygame.font.SysFont("comicsans", 15)

    easy = fnt.render("Easy", 1, (0, 0, 0))
    normal = fnt.render("Normal", 1, (0, 0, 0))
    hard = fnt.render("Hard", 1, (0, 0, 0))

    easy_rect = pygame.Rect(600, 210, 65, 30)
    nor_rect = pygame.Rect(600, 250, 65, 30)
    hard_rect = pygame.Rect(600, 290, 65, 30)

    buttons = [
        [easy, easy_rect, (255, 255, 255)],
        [normal, nor_rect, (185, 190, 195)],
        [hard, hard_rect, (255, 255, 255)]
    ]

    return buttons


def setup_options():
    # function to set up various options available to the user
    fnt = pygame.font.SysFont("comicsans", 15)
    solve_text = fnt.render("Solve", 1, (0, 0, 0))
    new_puzzle = fnt.render("New Puzzle", 1, (0, 0, 0))
    show_sol = fnt.render("Show Solution", 1, (0, 0, 0))
    show_hint = fnt.render("Hint", 1, (0, 0, 0))

    solve_rect = pygame.Rect(550, 10, 150, 30)
    new_rect = pygame.Rect(550, 50, 150, 30)
    show_rect = pygame.Rect(550, 90, 150, 30)
    hint_rect = pygame.Rect(550, 130, 150, 30)

    buttons = [
        [solve_text, solve_rect, (255, 255, 255)],
        [new_puzzle, new_rect, (255, 255, 255)],
        [show_sol, show_rect, (255, 255, 255)],
        [show_hint, hint_rect, (255, 255, 255)]
    ]

    return buttons


def main():
    win = pygame.display.set_mode((725, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, GridGenerator, 540, 540, win, 3)
    options = setup_options()
    difficulty = setup_difficulty()

    solution_shown = False
    key = None
    run = True
    start = time.time()
    finish = False
    strikes = 0
    hints = 5
    while run:
        play_time = (round(time.time() - start))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                elif event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                elif event.key == pygame.K_SPACE:
                    if board.solve_gui():
                        finish = True
                elif event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0 and not solution_shown:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game Over!")
                            game_won(win, board, play_time, strikes, options, difficulty, hints)
                            finish = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if options[0][1].collidepoint(pos[0], pos[1]):
                    solve_start = time.time()
                    if board.solve_gui():
                        game_won(win, board, round(time.time() - solve_start), strikes, options, difficulty, hints)
                        finish = True
                elif options[1][1].collidepoint(pos[0], pos[1]):
                    cur_diff = board.get_difficulty()
                    board.generate_new_board(GridGenerator, cur_diff)
                    hints = 5
                    start = time.time()
                    finish = False
                elif options[2][1].collidepoint(pos[0], pos[1]):
                    fnt = pygame.font.SysFont("comicsans", 15)
                    if not solution_shown:
                        solution_shown = True
                        options[2][0] = fnt.render("Hide Solution", 1, (0, 0, 0))
                        redraw_window(win, board, play_time, strikes, options, difficulty, hints)
                        pygame.display.update()
                        show_solution(win, board)
                    else:
                        solution_shown = False
                        options[2][0] = fnt.render("Show Solution", 1, (0, 0, 0))
                elif options[3][1].collidepoint(pos[0], pos[1]) and hints > 0:
                    if board.hint_user():
                        hints -= 1
                elif difficulty[0][1].collidepoint(pos[0], pos[1]) and board.get_difficulty() != 1:
                    board.generate_new_board(GridGenerator, 1)
                    highlight_diff(difficulty, difficulty[0])
                    start = time.time()
                    hints = 5
                elif difficulty[1][1].collidepoint(pos[0], pos[1]) and board.get_difficulty() != 3:
                    board.generate_new_board(GridGenerator, 3)
                    highlight_diff(difficulty, difficulty[1])
                    start = time.time()
                    hints = 5
                elif difficulty[2][1].collidepoint(pos[0], pos[1]) and board.get_difficulty() != 5:
                    board.generate_new_board(GridGenerator, 5)
                    highlight_diff(difficulty, difficulty[2])
                    start = time.time()
                    hints = 5
                else:
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
            elif event.type == pygame.MOUSEMOTION:
                for option in options:
                    if option[1].collidepoint(event.pos):
                        option[2] = (185, 190, 195)
                    else:
                        option[2] = (255, 255, 255)

        if board.selected and key != None:
            board.sketch(key)

        if not finish and not solution_shown:
            redraw_window(win, board, play_time, strikes, options, difficulty, hints)
            pygame.display.update()


main()
pygame.quit()
