# terminal_sudoku.py

from copy import deepcopy


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


def print_board(board):
    print("\n    1 2 3   4 5 6   7 8 9")
    print("  +-------+-------+-------+")
    for r in range(9):
        row_values = []
        for c in range(9):
            value = board[r][c]
            row_values.append(str(value) if value != 0 else ".")

        print(
            f"{r + 1} | {' '.join(row_values[0:3])} | "
            f"{' '.join(row_values[3:6])} | {' '.join(row_values[6:9])} |"
        )

        if r in (2, 5, 8):
            print("  +-------+-------+-------+")
    print()


def is_valid_move(board, row, col, num):
    if any(board[row][c] == num for c in range(9)):
        return False
    if any(board[r][col] == num for r in range(9)):
        return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    return True


def find_empty_cell(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def solve_board(board):
    empty = find_empty_cell(board)
    if empty is None:
        return True

    row, col = empty
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_board(board):
                return True
            board[row][col] = 0
    return False


def board_is_complete(board):
    return all(cell != 0 for row in board for cell in row)


def command_help():
    print(
        "Commands:\n"
        "  set <row> <col> <num>   Place a number (1-9)\n"
        "  clear <row> <col>       Clear a non-fixed cell\n"
        "  check                   Validate current board state\n"
        "  solve                   Solve puzzle instantly\n"
        "  help                    Show commands\n"
        "  quit                    Exit game\n"
    )


def parse_three_ints(parts):
    if len(parts) != 4:
        return None
    try:
        return int(parts[1]), int(parts[2]), int(parts[3])
    except ValueError:
        return None


def parse_two_ints(parts):
    if len(parts) != 3:
        return None
    try:
        return int(parts[1]), int(parts[2])
    except ValueError:
        return None


def is_consistent(board):
    for row in board: # Check rows
        values = [v for v in row if v != 0]
        if len(values) != len(set(values)):
            return False

    for c in range(9): # Check columns
        values = [board[r][c] for r in range(9) if board[r][c] != 0]
        if len(values) != len(set(values)):
            return False

    for box_r in range(0, 9, 3): # Check 3x3 boxes
        for box_c in range(0, 9, 3):
            values = []
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    value = board[r][c]
                    if value != 0:
                        values.append(value)
            if len(values) != len(set(values)):
                return False

    return True


def main():
    board = deepcopy(START_BOARD)
    fixed_cells = {(r, c) for r in range(9) for c in range(9) if board[r][c] != 0}

    print("Sudoku (terminal)")
    print("Use 1-based row/col coordinates. Type 'help' for commands.")
    print_board(board)

    while True:
        raw = input("> ").strip().lower()
        if not raw:
            continue

        parts = raw.split()
        command = parts[0]

        if command == "quit":
            print("Goodbye.")
            break

        if command == "help":
            command_help()
            continue

        if command == "set":
            parsed = parse_three_ints(parts)
            if parsed is None:
                print("Usage: set <row> <col> <num>")
                continue

            row, col, num = parsed
            row -= 1
            col -= 1
            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                print("Row/col must be 1-9 and number must be 1-9.")
                continue
            if (row, col) in fixed_cells:
                print("That cell is fixed and cannot be changed.")
                continue

            old_value = board[row][col]
            board[row][col] = 0
            if not is_valid_move(board, row, col, num):
                board[row][col] = old_value
                print("Invalid move: conflicts with row, column, or 3x3 box.")
                continue

            board[row][col] = num
            print_board(board)

            if board_is_complete(board) and is_consistent(board):
                print("Nice! You solved the puzzle.")
                break
            continue

        if command == "clear":
            parsed = parse_two_ints(parts)
            if parsed is None:
                print("Usage: clear <row> <col>")
                continue

            row, col = parsed
            row -= 1
            col -= 1
            if not (0 <= row < 9 and 0 <= col < 9):
                print("Row/col must be 1-9.")
                continue
            if (row, col) in fixed_cells:
                print("That cell is fixed and cannot be cleared.")
                continue

            board[row][col] = 0
            print_board(board)
            continue

        if command == "check":
            if is_consistent(board):
                print("Current board is valid so far.")
            else:
                print("Current board has conflicts.")
            continue

        if command == "solve":
            work = deepcopy(board)
            if not solve_board(work):
                print("No solution exists from current board state.")
                continue
            board = work
            print_board(board)
            print("Solved.")
            break

        print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
