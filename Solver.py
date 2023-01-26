import math
import collections
from collections import namedtuple

N = 9


def PrintSudoku(sudoku):
    """runs throughout all the sudoku and prints its values

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    """
    for i in range(N):
        for j in range(N):
            print(str(sudoku[i][j]), end=" ")
        print()


def CheckEmptySpace(sudoku):
    """finds the first empty space (value 0) and returns index , returns -1,-1 if space not found

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    :return : index if empty space or -1,-1 if not found
    """
    for i in range(N):
        for j in range(N):
            if sudoku[i][j] == 0:
                return i, j
    return -1,-1


def CheckRow(sudoku, row, num):
    """goes throughout the row and looks for a duplicate of a given number

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    :param row: row index
    :type row: int
    :param num: number to look for
    :type num: int
    :return: true if not found , false if found
    """
    for col in range(N):
        if sudoku[row][col] == num:
            return False
    return True


def CheckCol(sudoku, col, num):
    """goes throughout the column and looks for a duplicate of a given number

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    :param col: column index
    :type col: int
    :param num: number to look for
    :type num: int
    :return: true if not found , false if found
    """
    for row in range(N):
        if sudoku[row][col] == num:
            return False
    return True


def CheckGrid(sudoku, row, col, num):
    """goes throughout the grid and looks for a duplicate of a given number

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    :param row: row index
    :type row: int
    :param col: column index
    :type row: int
    :param num: number to look for
    :type num: int
    :return: true if not found , false if found
    """
    gridRow = (row//math.isqrt(N))*math.isqrt(N)
    gridCol = (col // math.isqrt(N)) * math.isqrt(N)
    for i in range(math.isqrt(N)):
        for j in range(math.isqrt(N)):
            if sudoku[i+gridRow][j+gridCol] == num and sudoku[i+gridRow][j+gridCol] != sudoku[row][col]:
                return False
    return True


def CheckIfLegal(sudoku, row, col, num):
    """checks if not found a given number in row,col and grid

    :param sudoku: sudoku board
    :type sudoku: list (int*int)
    :param row: row index
    :type row: int
    :param col: column index
    :type row: int
    :param num: number to look for
    :type num: int
    :return: true if not found , false if found
    """
    return CheckRow(sudoku, row, num) and CheckCol(sudoku, col, num) and CheckGrid(sudoku, row, col, num)


def SudokuSolver(sudoku, moves=None):
    """A recursive function that solves a Sudoku

    It starts from the first blanc space and enters a loop.
    Starts from 1, picks it and enters the function recursively to look for the next blanc space.
    If the picked number is illegal then goes through the loop again and gives the next number.
    If the loop ended and all the numbers didn't fit , then return to the previous entered number and continue its loop.
    The function ends when it reaches last index in the Sudoku

    :param sudoku: a given matrix with numbers (0 in the empty places)
    :type sudoku: list (int*int)
    :param moves: a list given by the GUI program to write all the moves there to later on show them (default is None)
    :type moves: list (int*int)
    :return: true if Sudoku was solved , false if not
    """
    row, col = CheckEmptySpace(sudoku)
    cube = namedtuple('Cube', ['row', 'col', 'num', 'color'])
    if row == -1 and col == -1:
        if moves is not None:
            moves.reverse()
        return True

    for num in range(1, N+1):
        if CheckIfLegal(sudoku, row, col, num):
            sudoku[row][col] = num
            if moves is not None:
                newC = cube(row, col, num, True)
                moves.append(newC)
            if SudokuSolver(sudoku, moves):
                return True
            sudoku[row][col]=0
            if moves is not None:
                newC = cube(row, col, num, False)
                moves.append(newC)
    return False


