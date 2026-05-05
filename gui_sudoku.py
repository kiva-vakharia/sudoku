# sudoku_main.py
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 120, 255)
LIGHT_BLUE = (220, 232, 255)
RED = (190, 30, 30)
GRAY = (90, 90, 90)

WIDTH, HEIGHT = 600, 660
GRID_LEFT, GRID_TOP = 30, 20
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9

START_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

BOARD = [row[:] for row in START_BOARD]
FIXED_CELLS = {(r, c) for r in range(9) for c in range(9) if START_BOARD[r][c] != 0}
selected_cell = None
status_text = "Click a cell, then press 1-9. Backspace/Delete clears."
status_color = GRAY


def is_valid_move(board, row, col, value):
    if any(board[row][c] == value for c in range(9)):
        return False
    if any(board[r][col] == value for r in range(9)):
        return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == value:
                return False

    return True


def board_is_complete(board):
    return all(cell != 0 for row in board for cell in row)


def draw_grid(window):
    pygame.draw.rect(window, BLACK, (GRID_LEFT, GRID_TOP, GRID_SIZE, GRID_SIZE), 3)
    for i in range(1, 9):
        line_w = 3 if i % 3 == 0 else 1
        x = GRID_LEFT + i * CELL_SIZE
        y = GRID_TOP + i * CELL_SIZE
        pygame.draw.line(window, BLACK, (x, GRID_TOP), (x, GRID_TOP + GRID_SIZE), line_w)
        pygame.draw.line(window, BLACK, (GRID_LEFT, y), (GRID_LEFT + GRID_SIZE, y), line_w)


def fill_board(window, board):
    font = pygame.font.Font(None, 44)
    for r in range(9):
        for c in range(9):
            value = board[r][c]
            if value == 0:
                continue

            is_fixed = (r, c) in FIXED_CELLS
            color = BLACK if is_fixed else BLUE
            text = font.render(str(value), True, color)
            text_x = GRID_LEFT + c * CELL_SIZE + 20
            text_y = GRID_TOP + r * CELL_SIZE + 12
            window.blit(text, (text_x, text_y))


def draw_selected(window):
    if selected_cell is None:
        return
    row, col = selected_cell
    rect = pygame.Rect(
        GRID_LEFT + col * CELL_SIZE,
        GRID_TOP + row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )
    pygame.draw.rect(window, LIGHT_BLUE, rect)
    pygame.draw.rect(window, BLUE, rect, 3)


def draw_status(window):
    font = pygame.font.Font(None, 30)
    msg = font.render(status_text, True, status_color)
    window.blit(msg, (GRID_LEFT, GRID_TOP + GRID_SIZE + 30))


def draw(window):
    window.fill(WHITE)
    draw_selected(window)
    draw_grid(window)
    fill_board(window, BOARD)
    draw_status(window)
    pygame.display.update()


def set_status(message, color=GRAY):
    global status_text, status_color
    status_text = message
    status_color = color


def handle_mouse():
    global selected_cell
    x, y = pygame.mouse.get_pos()
    inside_x = GRID_LEFT <= x < GRID_LEFT + GRID_SIZE
    inside_y = GRID_TOP <= y < GRID_TOP + GRID_SIZE
    if not (inside_x and inside_y):
        selected_cell = None
        return

    col = (x - GRID_LEFT) // CELL_SIZE
    row = (y - GRID_TOP) // CELL_SIZE
    selected_cell = (row, col)


def try_set_value(key):
    if selected_cell is None:
        set_status("Select a cell first.", RED)
        return

    row, col = selected_cell
    if (row, col) in FIXED_CELLS:
        set_status("That is a fixed cell.", RED)
        return

    if not (pygame.K_1 <= key <= pygame.K_9):
        return

    value = key - pygame.K_0
    old_value = BOARD[row][col]
    BOARD[row][col] = 0
    if not is_valid_move(BOARD, row, col, value):
        BOARD[row][col] = old_value
        set_status("Invalid move.", RED)
        return

    BOARD[row][col] = value
    if board_is_complete(BOARD):
        set_status("Solved! Nice work.", BLUE)
    else:
        set_status("Number placed.")


def clear_selected_cell():
    if selected_cell is None:
        set_status("Select a cell first.", RED)
        return

    row, col = selected_cell
    if (row, col) in FIXED_CELLS:
        set_status("Cannot clear a fixed cell.", RED)
        return

    BOARD[row][col] = 0
    set_status("Cell cleared.")


def run_sudoku():
    pygame.init()
    pygame.display.set_caption("Sudoku - Basic GUI")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_mouse()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    clear_selected_cell()
                else:
                    try_set_value(event.key)

        draw(window)
        clock.tick(60)

    pygame.quit()
    sys.exit()


run_sudoku()