import pygame
import sys
import random
from itertools import chain

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FONTSIZE = CELL_SIZE // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame and font
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Arial", FONTSIZE)

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

import random

def generate_sudoku():
    # Create an empty 9x9 grid
    grid = [[0 for x in range(9)] for y in range(9)]

    # Fill the diagonal 3x3 grids with random numbers
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for k in range(3):
                for l in range(3):
                    grid[i+k][j+l] = nums.pop()

    # Solve the grid
    solve_sudoku(grid)

    # Remove some numbers from the grid to create the puzzle
    num_remove = random.randint(30, 50)
    for i in range(num_remove):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while grid[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        grid[row][col] = 0

    return grid

def solve_sudoku(grid):
    # Find the next empty cell
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True

    row, col = empty_cell

    # Try each number from 1 to 9 in the cell
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0

    # If none of the numbers worked, backtrack
    return False

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False

    # Check column
    if num in [grid[i][col] for i in range(9)]:
        return False

    # Check 3x3 grid
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if grid[i][j] == num:
                return False

    # If none of the checks failed, it's a valid move
    return True



grid = generate_sudoku()
initial_grid = [row.copy() for row in grid]

def draw_grid():
    for i in range(0, 10):
        thickness = 1
        if i % 3 == 0:
            thickness = 3
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thickness)

    for y, row in enumerate(grid):
        for x, num in enumerate(row):
            if num != 0:
                color = BLACK if initial_grid[y][x] != 0 else GREEN
                if color == GREEN and not is_valid_move(x, y, grid[x][y]):
                    color = RED
                num_text = FONT.render(str(num), True, color)
                screen.blit(num_text, (x * CELL_SIZE + FONTSIZE // 4, y * CELL_SIZE + FONTSIZE // 4))

def is_valid_move(x, y, num):
    if num in grid[y]:
        return False
    if num in [row[x] for row in grid]:
        return False

    box_x, box_y = x // 3, y // 3
    for i in range(3):
        for j in range(3):
            if grid[box_y * 3 + i][box_x * 3 + j] == num:
                return False

    return True

def check_win():
    return all(0 not in row for row in grid)

def main():
    selected_cell = None
    input_num = None
    running = True
    game_won = False
    while running:
        screen.fill(WHITE)
        draw_grid()

        if game_won:
            win_text = FONT.render("Congratulations! You've completed the Sudoku!", True, RED)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.unicode.isdigit():
                    input_num = int(event.unicode)

                if selected_cell is not None and input_num is not None and initial_grid[selected_cell[1]][selected_cell[0]] == 0:
                    x, y = selected_cell
                    grid[y][x] = input_num
                    input_num = None
                    selected_cell = None
                    game_won = check_win()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x, y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                selected_cell = (x, y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()

