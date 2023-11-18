# sudoku_solver
A sudoku solver program using pygame and python

![alt text](https://github.com/ShaneGaymon28/sudoku_solver/blob/main/images/sudoku_solver_screenshot.png "Sudoku Solver")


## How to Run
You can run the program by opening a terminal and typing `python3 GUI.py` 

## How to Play
* Sudoku instructions - [https://masteringsudoku.com/sudoku-rules-beginners/]
* Upon running the program, the game automatically generates a board and starts the game
* Select an empty square (square will highlight red once selected) and type a number to place a temporary value in that square
* Press RETURN to attempt to add the temporary value in that square
* NOTE: if the value you attempt to add is wrong, it will not be added and you will gain a strike
* To delete a temp value: select the square and press the DEL key
* Along with the Solve menu option, you can use the SPACE bar to have the computer solve the puzzle

### Menu Options
* Solve: solves the current puzzle using a recursive / backtracking algorithm
* New Puzzle: generates a new, unique puzzle board
* Show/Hide Solution: shows the COMPLETE solution to the user (NOTE: you must hide the solution to continue entering values into the puzzle)
* Hint: randomly reveal one CORRECT square in the puzzle (NOTE: you are allowed 5 per game)
* Difficulty: selects the difficulty for the puzzle (easy, medium, or hard)

## Features
* Generate a new, valid sudoku puzzle
* Solve the current puzzle for the user using a recursive/backtracking algorithm
* View the solution
* Ask for a hint! (You only get 5 so use them carefully)
* Change the difficulty (easy, medium, or hard)


