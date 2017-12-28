#!/usr/bin/env python3


# 8 queens puzzle (https://en.wikipedia.org/wiki/Eight_queens_puzzle) solver.
# Finds a solution using the backtracking algorithm and prints it to a console.

BOARD_SIZE = 8


def print_board(board):
    for row_idx in range(BOARD_SIZE):
        row_str = ' '.join(map(lambda x: 'Q' if x else '_', board[row_idx]))
        print(row_str)


def is_configuration_valid(board):
    for row_idx in range(BOARD_SIZE):
        for col_idx in range(BOARD_SIZE):
            has_queen = board[row_idx][col_idx]
            if has_queen:
                for i in range(BOARD_SIZE):
                    if i != row_idx and board[i][col_idx]:
                        # Check other cells in the same column.
                        return False
                    if i != col_idx and board[row_idx][i]:
                        # Check other cells in the same row.
                        return False
                    if i > 0:
                        # Check all possible diagonal cells.
                        diagonal_indexes = [
                            (row_idx - i, col_idx - i),
                            (row_idx + i, col_idx + i),
                            (row_idx - i, col_idx + i),
                            (row_idx + i, col_idx - i),
                        ]
                        for diag_row, diag_col in diagonal_indexes:
                            if 0 <= diag_row < BOARD_SIZE and 0 <= diag_col < BOARD_SIZE and board[diag_row][diag_col]:
                                return False
    return True


def backtracking(board, col_idx=0):
    for row_idx in range(BOARD_SIZE):
        # Attempt to place a queen.
        board[row_idx][col_idx] = True

        if is_configuration_valid(board):
            next_col_idx = col_idx + 1
            if next_col_idx >= BOARD_SIZE:
                # All columns have been processed. The problem is solved.
                return True
            if backtracking(board, col_idx=next_col_idx):
                # The subsequent configuration is valid. Report success.
                return True
            else:
                # The solution can't be achieved in the current state. Revert this attempt.
                board[row_idx][col_idx] = False
        else:
            # Configuration is invalid. Revert this attempt and go to the next one.
            board[row_idx][col_idx] = False
    return False


def create_board():
    board = []
    for _ in range(BOARD_SIZE):
        board.append([False] * BOARD_SIZE)
    return board


def main():
    board = create_board()
    backtracking(board)
    print_board(board)


if __name__ == '__main__':
    main()
