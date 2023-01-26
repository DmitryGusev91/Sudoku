"""GUI of sudoku which implements the sudoku solver algorithm

This script allow the user to play sudoku on a graphical sudoku board , and when stuck or finished
watch how it solves itself with the help of 'Backtracking'

The starting function (main) accepts a missing sudoku (zeros in the missing spots)

This script requires 'pygame' be installed within the Python environment as well
as the copy library and the Solver library which contains the Backtracking algorithm

The file contains the following functions and classes:
    :class Cube: which works on an individual space(cube) in the sudoku
    :class Sudoku: which contains all the cube and implements the necessary actions
    :func menu: which initiates the pygame running loop and sends instructions to Sudoku according to the user

There are constant variables such as: cube size and amount of cubes each side
"""

from copy import deepcopy
import pygame
import Solver

CUBE_NUMBER = 9
CUBE_WIDTH = 50
CUBE_HEIGHT = 50


class Sudoku:
    """A class that represents the sudoku board

    :atr self.board: A matrix that has the current rightful sudoko( you can solve with this one)
    :type self.board: list (n*n of ints)
    :atr self.cubes: Cube objects located as the the board with the same coordinates
    :type self.cubes:list ( n*n of Cubes)
    :atr self.move_list: a list that contains the moves that the solving algorithm did (value,row,col)
    :type self.move_list: list ([(int,int,int),...])
    :atr self.auto: A flag that show if the algorithm is running or not
    :type self.auto: bool
    :atr self.tmp_board: A matrix (copy of self.board) that we can put values there and check if the algorithm can solve
     it (for manual picking)
    :type self.tmp_board: list (with int*int in it)

    :method __init__: Initiates the class
    :method update: Updates all the time the values (Cubes and board) depending on the status of the class(auto)
    :method update_tmp_board: Restores the tmp_board to it default position (copy of board)
    :method start_solving: Starts the backtracking algorithm and changes the status of the class to auto
    :method submit: Checks if the sudoku can be solved with the given number , and if yes then puts it on the board
    :method cleat_tmp: Removes the number that the user tried to enter

    :param board: the given sudoku (nXn of ints)
    :type board:list
    :param window:the surface of pygame that we draw on it
    :type window: pygame.display
    """
    def __init__(self, board, window):
        """Initiates the class"""
        self.board = board
        # copies values from the given sudoku
        self.cubes = [[Cube(board[row][col], row, col, window) for col in range(CUBE_NUMBER)]for
                      row in range(CUBE_NUMBER)]
        self.move_list = []
        self.auto = False
        self.tmp_board = []

    def update(self, pressed_keys, pressed_mouse, window):
        """Updates all the time the values (Cubes and board) depending on the status of the class(auto)

        If the auto is true (the algorithm is running) then it takes the moves from move_list and inserts and highlight
        the board accordingly, if not then updates each Cube individually and draws the thick lines ion the board

        :param pressed_keys: The next pressed button in the queue that need to do something
        :param pressed_mouse: The next pressed mouse button in the queue that need to do something
        :param window: The interface of pygame that we are working on
        """
        if self.auto and len(self.move_list) != 0:
            tmp = self.move_list.pop()
            row = tmp.row
            col = tmp.col
            num = tmp.num
            self.cubes[row][col].color = tmp.color
            self.cubes[row][col].is_pressed(window)
            self.cubes[row][col].set_value(num, False, window)
            # updates each cube individually and draws the thick lines on the board

        def should_draw_vertical(col):
            return col % (CUBE_NUMBER ** 0.5) == 1 and col != 1

        def should_draw_horizontal(row):
            return row % (CUBE_NUMBER ** 0.5) == 1 and row != 1

        [cube.update(pressed_keys, pressed_mouse, window) for row in self.cubes for cube in row]
        vertical = filter(should_draw_vertical,range(CUBE_NUMBER))
        horizontal = filter(should_draw_horizontal, range(CUBE_NUMBER))
        for col in vertical:
            pygame.draw.line(window, (0, 0, 0), ((col - 1) * CUBE_WIDTH, 0), ((col - 1) * CUBE_HEIGHT,
                                                                              CUBE_NUMBER * CUBE_WIDTH), 4)
        for row in horizontal:
            pygame.draw.line(window, (0, 0, 0), (0, (row - 1) * CUBE_HEIGHT),
                             (CUBE_NUMBER * CUBE_WIDTH, (row - 1) * CUBE_HEIGHT), 4)

        pygame.draw.line(window, (0, 0, 0), (0, CUBE_NUMBER*CUBE_HEIGHT),
                         (CUBE_NUMBER*CUBE_WIDTH, CUBE_WIDTH*CUBE_NUMBER), 4)

    def update_tmp_board(self):
        """Restores the tmp_board to it default position (copy of board)"""
        self.tmp_board = deepcopy(self.board)

    def start_solving(self):
        """Starts the backtracking algorithm and changes the status of the class to auto"""
        self.auto = True
        Solver.SudokuSolver(self.board, self.move_list)

    def submit(self, window):
        """Checks if the sudoku can be solved with the given number , and if yes then puts it on the board.

        If the algorithm isn't working, and the Cube is pressed , Cubes value isn't 0 and the entered number is legal
        then we may enter the number to the board and update all the boards else delete the users number and
        clear all the boards from it

        :param window: The interface of pygame that we are working on
        """
        self.update_tmp_board()
        if not self.auto:
            for i in range(CUBE_NUMBER):
                for j in range(CUBE_NUMBER):
                    if self.cubes[i][j].pressed and self.cubes[i][j].tmp_value != 0:
                        num = self.cubes[i][j].tmp_value
                        if Solver.CheckIfLegal(self.tmp_board, i, j, self.cubes[i][j].tmp_value):
                            self.tmp_board[i][j] = self.cubes[i][j].tmp_value
                            if Solver.SudokuSolver(self.tmp_board):
                                self.cubes[i][j].set_value(self.cubes[i][j].tmp_value, False,window)
                                self.cubes[i][j].is_unpress(window)
                                self.board[i][j] = num
                            else:
                                self.cubes[i][j].delete_value(window)
                        else:
                            self.cubes[i][j].delete_value(window)

    def clear_tmp(self, window):
        """Finds the targeted Cube and removes the number that the user tried to enter

        :param window: The interface of pygame that we are working on
        """
        def should_delete_value(cube):
            """returns if the button is pressed and tmp is not 0"""
            return cube.pressed and cube.tmp_value != 0

        list(map(lambda cube: cube.delete_value(window), filter(should_delete_value, [cube for row in self.cubes
                                                                                      for cube in row])))


class Cube:
    """A class that represents each cube in the Sudoku board

    :atr self.value: The VALID value for this cube
    :type self.value: int
    :atr self.row: row index
    :type self.row: int
    :atr self.col: column index
    :type self.col: int
    :atr self.pressed: A flag that show if the button is pressed
    :type self.pressed: bool
    :atr self.x: place of right top corner at the Sudoku board (pixel) in the X line
    :type self.x: int
    :atr self.y: place of right top corner at the Sudoku board (pixel) in the Y line
    :type self.y: int
    :atr self.rect: the object that the rectangle is
    :type self.rect: pygame.rect
    :atr self.color: the current color of the cube
    :type self.color: tuple(rgb)
    :atr self.tmp_value: the temporary index that the user has chose (starts with 0)
    :type self.tmp_value: int

    :method __init__: Initiates the class
    :method update: Updates all the time the values depending on the status of the class (pressed or no / has tmp number
     or no)
    :method is_unpressed: unpresses the button
    :method is_pressed: presses the button and if submits then highlights green , otherwise red
    :method delete_value: deletes the value
    :method set_value: sets the given value(tmp or final)

    :param value: given value to the Sudoku
    :type value: int
    :param row: row index
    :type row: int
    :param col: column index
    :type col: int
    :param window:the surface of pygame that we draw on it
    :type window: pygame.display
    """
    def __init__(self, value, row, col, window):
        """Initiates the class"""
        self.value = value
        self.row = row
        self.col = col
        self.pressed = False
        self.x = CUBE_WIDTH*self.col
        self.y = CUBE_HEIGHT*self.row
        self.rect = None
        self.color = False
        self.tmp_value = 0

        def draw():
            """draws the cube, the border (number if given)"""
            color = (0, 0, 0)
            if self.value != 0:
                font = pygame.font.SysFont('gadugi', 25)
                num_txt = font.render(str(self.value), True, (0, 0, 0))
                window.blit(num_txt, (self.x + CUBE_WIDTH / 2 - 5, self.y + CUBE_HEIGHT / 2 - 17))
            self.rect = pygame.draw.rect(window, color, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_HEIGHT), 1)

        draw()

    def is_unpress(self, window):
        """unpresses the button

        draws it white and then draw it normal

        :param window:the surface of pygame that we draw on it
        :type window: pygame.display
        """
        self.pressed = False
        color = (255, 255, 255)
        pygame.draw.rect(window, color, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_HEIGHT), 2)
        color = (0, 0, 0)
        pygame.draw.rect(window, color, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_HEIGHT), 1)

    def is_pressed(self, window):
        """presses the button and if submits then highlights green , otherwise red

        :param window:the surface of pygame that we draw on it
        :type window: pygame.display"""
        self.pressed = True
        if self.color:
            color = (0, 255, 0)
        else:
            self.is_unpress(window)
            self.pressed = True
            color = (255, 0, 0)
        pygame.draw.rect(window, color, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_HEIGHT), 2)

    def update(self, pressed_keys, pressed_mouse, window):
        """Updates all the time the values depending on the status of the class (pressed or no / has tmp number

        changes value depending on the keyboard button clicked (1-9) , and change to status 'pressed' when button is
        pressed with mouse

        :param pressed_keys:the key that was pressed
        :type pressed_keys: the key
        :param pressed_mouse: place of mouse click (x,y)
        :type pressed_mouse: tuple (int,int)
        :param window:the surface of pygame that we draw on it
        :type window: pygame.display
        """
        if self.pressed:
            self.is_pressed(window)
            if self.value == 0:
                if pressed_keys[pygame.K_1]:
                    self.set_value(1, True, window)
                elif pressed_keys[pygame.K_2]:
                    self.set_value(2, True, window)
                elif pressed_keys[pygame.K_3]:
                    self.set_value(3, True, window)
                elif pressed_keys[pygame.K_4]:
                    self.set_value(4, True, window)
                elif pressed_keys[pygame.K_5]:
                    self.set_value(5, True, window)
                elif pressed_keys[pygame.K_6]:
                    self.set_value(6, True, window)
                elif pressed_keys[pygame.K_7]:
                    self.set_value(7, True, window)
                elif pressed_keys[pygame.K_8]:
                    self.set_value(8, True, window)
                elif pressed_keys[pygame.K_9]:
                    self.set_value(9, True, window)
        else:
            self.is_unpress(window)
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < CUBE_NUMBER * CUBE_HEIGHT:
            if pressed_mouse[0]:
                if self.rect.collidepoint(mouse_pos):
                    self.color = False
                    self.pressed = True
                else:
                    self.pressed = False

    def delete_value(self, window):
        """deletes and resets the values

        :param window:the surface of pygame that we draw on it
        :type window: pygame.display"""
        self.rect = pygame.draw.rect(window, (255, 255, 255), pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_HEIGHT))
        if self.value == 0:
            self.tmp_value = 0

    def set_value(self, value, tmp, window):
        """
        sets the given value(tmp or final)

        :param value: the VALID value
        :type value: int
        :param tmp: the value given by the user
        :type tmp: int
        :param window:the surface of pygame that we draw on it
        :type window: pygame.display
        """
        self.delete_value(window)
        if tmp:
            self.tmp_value = value
            font = pygame.font.SysFont('gadugi', 23)
            num_txt = font.render(str(value), True, (192, 192, 192))
            window.blit(num_txt, (self.x + CUBE_WIDTH / 2 - 20, self.y + CUBE_HEIGHT / 2 - 25))
        else:
            self.value = value
            font = pygame.font.SysFont('gadugi', 25)
            num_txt = font.render(str(value), True, (0, 0, 0))
            window.blit(num_txt, (self.x + CUBE_WIDTH / 2 - 5, self.y + CUBE_HEIGHT / 2 - 17))


def menu(board):
    """The main function that starts all the program.

    It initiates the pygame , and the Sudoku board.
    Then runs a while loop in which it sends all the time users activities and changes the status of the board
    accordingly .
    """
    pygame.init()
    window = pygame.display.set_mode((CUBE_WIDTH * CUBE_NUMBER, CUBE_HEIGHT * CUBE_NUMBER + 100))
    pygame.display.set_caption('Sudoku Solver')
    window.fill((255, 255, 255))

    # Text with instructions for player at the bottom of the board
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = "Wellcome to my game!!!"
    num_txt = font.render(text, True, (0, 0, 0))
    window.blit(num_txt, (0, CUBE_NUMBER * CUBE_HEIGHT + 10))
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = " c = clear place   enter = place number   1-9 = numbers"
    num_txt = font.render(text, True, (0, 0, 0))
    window.blit(num_txt, (0, CUBE_NUMBER * CUBE_HEIGHT + 40))
    text = " lft mouse = pick a place   space = auto solve"
    num_txt = font.render(text, True, (0, 0, 0))
    window.blit(num_txt, (0, CUBE_NUMBER * CUBE_HEIGHT + 60))

    s = Sudoku(board, window)

    running = True
    while running:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not s.auto:
                    if event.key == pygame.K_SPACE:
                        s.start_solving()
                    if event.key == pygame.K_RETURN:
                        s.submit(window)
                    if event.key == pygame.K_c:
                        s.clear_tmp(window)

        # if the algorithm is running then cant play
        if not s.auto:
            pressed_keys = pygame.key.get_pressed()
            pressed_mouse = pygame.mouse.get_pressed()

        s.update(pressed_keys, pressed_mouse, window)
        pygame.display.flip()


# The given board (can be changed)
board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]
menu(board)
