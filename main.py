import numpy as np
import pygame
import sys
import math
import numbers

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
game_over = False
turn = 0
CELLSIZE = 100
RADIUS = int(CELLSIZE / 2 - 5)
ROWCOUNT = 6
COLUMNCOUNT = 7
width = COLUMNCOUNT * CELLSIZE
height = (ROWCOUNT + 1) * CELLSIZE


# Draws the connect 4 board
def draw_board(board):
    flipped = np.flip(board, 0)
    for c in range(COLUMNCOUNT):
        for r in range(ROWCOUNT):
            pygame.draw.rect(screen, BLUE, (c * CELLSIZE, r * CELLSIZE + CELLSIZE, CELLSIZE, CELLSIZE))
            pygame.draw.circle(screen, BLACK, (int(c*CELLSIZE+CELLSIZE/2), int(r*CELLSIZE+CELLSIZE+CELLSIZE/2)), RADIUS)

    for c in range(COLUMNCOUNT):
        for r in range(ROWCOUNT):
            if flipped[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (int(c * CELLSIZE + CELLSIZE / 2), height - int(r * CELLSIZE + CELLSIZE / 2)),
                                   RADIUS)
            elif flipped[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(c * CELLSIZE + CELLSIZE / 2), height - int(r * CELLSIZE + CELLSIZE / 2)),
                                   RADIUS)

    pygame.display.update()


def is_full(board, col):
    # TODO return whether column has any empty spots left
    return last_zero(board)[col] == -1


# 0 - empty, 1 - red, 2-blue
def create_board():
    return np.zeros((ROWCOUNT, COLUMNCOUNT))


# Find available space on each column (0 closest to the bottom in each column)
def last_zero(arr, axis=0, invalid_val=-1):
    mask = arr == 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


# CheckWin, 1 - red, 2 - blue
def checkWin(arr):
    winRed = [1, 1, 1, 1]
    winBlue = [2, 2, 2, 2]

    checkArr = [arr[i:i + 4] for i in range(len(arr) - 3)]

    for check in checkArr:
        if np.array_equal(winRed, check):
            return 1
        elif np.array_equal(winBlue, check):
            return 2
    return 0


# CheckWin  - Negative Diagonal
def neg_diag_win(arr):
    winRed = ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])
    winBlue = ([2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2])


# CheckWin - Positive Diagonal
def pos_diag_win(arr):
    winRed = np.array([1, 1, 1, 1])
    winBlue = np.array([2, 2, 2, 2])

    for i in range(len(arr) - 3):
        for j in range(len(arr[0]) - 3):
            ixgrid = np.ix_([i, i + 1, i + 2, i + 3], [j, j + 1, j + 2, j + 3])
            checkArr = np.flipud(arr[ixgrid])
            checkArr = np.diag(checkArr)
            if np.array_equal(winRed, checkArr):
                return 1
            if np.array_equal(winBlue, checkArr):
                return 2

    return 0


# Starts game
board = create_board()
screen = pygame.display.set_mode((700, 700))
draw_board(board)
pygame.init()

pygame.display.update()

font = pygame.font.SysFont("Times New Roman", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, CELLSIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(CELLSIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(CELLSIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, CELLSIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / CELLSIZE))

                if not is_full(board, col):
                    row = last_zero(board)[col]
                    board[row][col] = 1
                    turn += 1
                    turn = turn % 2

                    if checkWin(board):
                        print("player 1 wins")
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / CELLSIZE))
                if not is_full(board, col):
                    row = last_zero(board)[col]
                    board[row][col] = 2
                    turn += 1
                    turn = turn % 2

                if checkWin(board):
                    print("player 2 wins")
                    game_over = True

            draw_board(board)



            if game_over:
                sys.exit()
