import numpy as np
import math
from random import choice
import os


def create_board(n, m):
    board = np.zeros((n, m), dtype=int)
    return board


def make_move(board, column, letter):
    for i in reversed(range(len(board))):
        if board[i, column] == 0:
            board[i, column] = letter
            return board


def get_possible_move(board):
    possible_moves = []
    for i, column in enumerate(board[0]):
        if column == 0:
            possible_moves.append(i)
    return possible_moves


def check_win(board, letter):
    for row in range(len(board)):
        for column in range(len(board[0]) - 3):
            if np.all(board[row, column:column+4] == letter):
                return True

    for column in range(len(board[0])):
        for row in range(len(board)-3):
            if np.all(board[row:row+4, column] == letter):
                return True

    for row in range(len(board)-3):
        for column in range(len(board[0]) - 3):
            if np.all(board[row:row+4, column:column+4].diagonal() == letter):
                return True

    for row in range(len(board) - 3, len(board)):
        for column in range(len(board[0]) - 3):
            if np.all(np.flipud(board[row-3:row+1,
                                      column:column+4]).diagonal() == letter):
                return True

    return False


def is_terminal(board, p_move, letter):
    new_board = board.copy()
    make_move(new_board, p_move, letter)
    return check_win(new_board, letter)


def minimax_tree(board, depth, player):
    if depth == 0 or check_win(board, 1) or check_win(board, 2) or\
          np.all(board != 0):
        if check_win(board, 1):
            return 1
        elif check_win(board, 2):
            return -1
        else:
            return 0
    if player == "max":
        max_eval = -math.inf
        for move in get_possible_move(board):
            new_board = board.copy()
            make_move(new_board, move, 1)
            evaluate = minimax_tree(new_board, depth-1, 'min')
            max_eval = max(evaluate, max_eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in get_possible_move(board):
            new_board = board.copy()
            make_move(new_board, move, 2)
            evaluate = minimax_tree(new_board, depth-1, 'max')
            min_eval = min(min_eval, evaluate)
        return min_eval


def best_move(board, depth):
    values = [(-math.inf, -math.inf)]
    for move in get_possible_move(board):
        if is_terminal(board, move, 1):
            return move
        new_board = board.copy()
        make_move(new_board, move, 1)
        value = minimax_tree(new_board, depth - 1, 'min')
        if value > max(values)[0]:
            values = [(value, move)]
        elif value == max(values)[0]:
            values.append((value, move))
    return choice(values)[1]


def print_board(board):
    for row in board:
        print('| ', end='')
        for char in row:
            if char == 1:
                print('\033[93mO\033[0m | ', end='')
            elif char == 2:
                print('\033[32mX\033[0m | ', end='')
            else:
                print(f'{char} | ', end='')
        print()


def main():
    b = create_board(7, 6)
    while not check_win(b, 1) and not check_win(b, 2) and not np.all(b != 0):
        os.system('cls')
        print_board(b)
        p_move = int(input("Choose move: "))
        make_move(b, p_move, 2)
        if check_win(b, 2):
            break
        ai_move = best_move(b, 2)
        make_move(b, ai_move, 1)
    if check_win(b, 1):
        print('\033[31mComputer win!\033[0m')
    elif check_win(b, 2):
        print('\033[31mYou win!\033[0m')
    print_board(b)


if __name__ == '__main__':
    main()
