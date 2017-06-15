from copy import deepcopy
import board as board
import numpy as np
import time

def expectimax(node, depth):
    alpha = None
    if depth == 0 or node.check_board():
        return heuristic(node)

    elif depth % 2 == 1:
        alpha = float('-inf')
        moveset = ['up', 'down', 'left', 'right']
        for move in moveset:
            child = deepcopy(node)
            child.move_board(move)
            if np.array_equal(node.get_board(), child.get_board()):
                continue
            alpha = max(alpha, expectimax(child, depth - 1))
    elif depth % 2 == 0:
            board = node.get_board()
            children = []
            for x in range(4):
                for y in range(4):
                    if board[x][y] == 0:
                        children.append((x,y))
            alpha = 0.0
            if len(children) == 0:
                alpha = expectimax(node, depth - 1)
            else:
                prob_of_2 = .9 / len(children)
                prob_of_4 = .1 / len(children)
                for pos in children:
                    child = deepcopy(node)
                    board = child.get_board()
                    board[pos[0]][pos[1]] = 2
                    child.set_board(board)
                    alpha += prob_of_2 * expectimax(child, depth - 1)
                    board[pos[0]][pos[1]] = 4
                    child.set_board(board)
                    alpha += prob_of_4 * expectimax(child, depth - 1)

    return alpha

def heuristic(node):
    if node.check_board():
        return -10000000000.0

    empty = float(node.get_empty())
    board = node.get_board()
    val = 0.0
    for i in range(3):
        for j in range(3):
            if board[i][j] >= board[i][j+1]:
                val += board[i][j]
            else:
                val -= abs(board[i][j] - board[i][j+1])

            if board[i][j] >= board[i+1][j]:
                val += board[i][j]
            else:
                val -= abs(board[i][j] - board[i+1][j])

    sub = 1.0
    #.6, .5, .1, .01
    if empty == 3:
        sub = .9
    elif empty == 2:
        sub = .8
    elif empty == 1:
        sub = .7
    elif empty == 0:
        sub = .6
    return val * sub

board = board.Board()
board.print_board()
print()

while True:
    best_move = None
    best_alpha = float('-inf')
    moveset = ['up', 'down', 'left', 'right']
    for move in moveset:
        t = time.time()
        test = deepcopy(board)
        test.move_board(move)
        if np.array_equal(test.get_board(), board.get_board()):
            print("continuing...")
            continue
        alpha = expectimax(test, 4)
        if time.time() - t < .05:
            alpha = expectimax(test, 6)
        if alpha > best_alpha:
            best_alpha = alpha
            best_move = move
    board.move_board(best_move)
    board.print_board()
    print()
    if board.check_board():
        print("You Lose!")
        break
