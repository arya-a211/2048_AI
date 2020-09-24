import time

import pygame, sys
import statistics
from pygame.locals import *
from colours import *
from random import *
from copy import deepcopy

TOTAL_POINTS = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4
GAMES_TO_FINISH_PER_STATE = 100
pygame.init()

SURFACE = pygame.display.set_mode((600, 700), 0, 32)
pygame.display.set_caption("2048")

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []
all_moves = [[], [], [], []]


# we need to copy total point and tile matrix before doing the loop
def finish_one_game(tm, tp):
    global TOTAL_POINTS, tileMatrix
    TOTAL_POINTS = 0
    first_move, fm_done = randint(0, 3), False
    while True:
        if not fm_done:
            rnd_move = first_move
            fm_done = True
        else:
            rnd_move = randint(0, 3)
        if check_if_can_go():  # TAKE THE MOVE
            rotations = rnd_move

            for i in range(0, rotations):
                rotate_matrix_clockwise()

            if can_move():
                move_tiles()
                merge_tiles()
                place_random_tile()

            for j in range(0, (4 - rotations) % 4):
                rotate_matrix_clockwise()

        else:
            all_moves[first_move].append(TOTAL_POINTS)
            tileMatrix = deepcopy(tm)  
            TOTAL_POINTS = tp
            break


def main():
    global all_moves
    place_random_tile()
    place_random_tile()

    print_matrix()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        tile_matrix_copy, total_points_copy = deepcopy(tileMatrix), TOTAL_POINTS
        for i in range(GAMES_TO_FINISH_PER_STATE):
            finish_one_game(tile_matrix_copy, total_points_copy)
        best_move = return_best_move()
        all_moves = [[], [], [], []]
        if check_if_can_go():
            rotations = best_move

            for i in range(0, rotations):
                rotate_matrix_clockwise()

            if can_move():
                move_tiles()
                merge_tiles()
                place_random_tile()

            for j in range(0, (4 - rotations) % 4):
                rotate_matrix_clockwise()

            print_matrix()
        else:
            printGameOver()
            time.sleep(3)
            sys.exit(0)

        pygame.display.update()


def print_matrix():
    SURFACE.fill(BLACK)

    global BOARD_SIZE
    global TOTAL_POINTS

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            pygame.draw.rect(SURFACE, get_colour(tileMatrix[i][j]),
                             (i * (600 / BOARD_SIZE), j * (600 / BOARD_SIZE) + 100, 600 / BOARD_SIZE, 600 / BOARD_SIZE))

            label = myfont.render(str(tileMatrix[i][j]), 1, WHITE)
            label2 = scorefont.render("Score: " + str(TOTAL_POINTS), 1, WHITE)

            offset = 0

            if tileMatrix[i][j] < 10:
                offset = -10
            elif tileMatrix[i][j] < 100:
                offset = -15
            elif tileMatrix[i][j] < 1000:
                offset = -20
            else:
                offset = -25

            if tileMatrix[i][j] > 0:
                SURFACE.blit(label, (i * (600 / BOARD_SIZE) + (300 / BOARD_SIZE) + offset,
                                     j * (600 / BOARD_SIZE) + 100 + 300 / BOARD_SIZE - 15))
            SURFACE.blit(label2, (10, 20))


def printGameOver():
    global TOTAL_POINTS

    SURFACE.fill(BLACK)

    label = scorefont.render("Game Over!", 1, (255, 255, 255))
    label2 = scorefont.render("Score: " + str(TOTAL_POINTS), 1, (255, 255, 255))
    label3 = myfont.render("Press r to restart!", 1, (255, 255, 255))

    SURFACE.blit(label, (150, 100))
    SURFACE.blit(label2, (150, 300))
    SURFACE.blit(label3, (150, 500))


def place_random_tile():
    count = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                count += 1

    k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:
        k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2


def floor(n):
    return int(n - (n % 1))


def move_tiles():
    # We want to work column by column shifting up each element in turn.
    for i in range(0, BOARD_SIZE):  # Work through our 4 columns.
        for j in range(0, BOARD_SIZE - 1):  # Now consider shifting up each element by checking top 3 elements if 0.
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][
                                                j:]) > 0:
                # If any element is 0 and there is a number to shift we want to shift up elements below.
                for k in range(j, BOARD_SIZE - 1):  # Move up elements below.
                    tileMatrix[i][k] = tileMatrix[i][k + 1]  # Move up each element one.
                tileMatrix[i][BOARD_SIZE - 1] = 0


def merge_tiles():
    global TOTAL_POINTS

    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k] * 2
                tileMatrix[i][k + 1] = 0
                TOTAL_POINTS += tileMatrix[i][k]
                move_tiles()


def check_if_can_go():
    for i in range(0, BOARD_SIZE ** 2):
        if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
            return True

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][j] == tileMatrix[i][j + 1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
                return True
    return False


def can_move():
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if tileMatrix[i][j - 1] == 0 and tileMatrix[i][j] > 0:
                return True
            elif (tileMatrix[i][j - 1] == tileMatrix[i][j]) and tileMatrix[i][j - 1] != 0:
                return True

    return False


def rotate_matrix_clockwise():
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4


def is_arrow(k):
    return k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT


def get_rotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


def convert_to_linear_matrix():
    mat = []

    for i in range(0, BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

    mat.append(TOTAL_POINTS)

    return mat


def return_best_move():
    """give a list containing a separate list for each of the possible moves (is either 0 (up), 1(left)
    , 2 (down), 3 (right), the mean of the end score per starting move is calculated, then we return the best move"""
    highest_average = 0
    best_move = -1
    for i in range(4):
        mean = statistics.mean(all_moves[i])
        if mean > highest_average:
            highest_average = mean
            best_move = i
    return best_move


main()
