from random import randint
import getch
import numpy as np
from copy import deepcopy
import random

class Board:
    def __init__(self):
        init_board = [0 for i in range(16)]
        count = 0
        while count < 2:
            pos = randint(0,15)
            if init_board[pos] == 0:
                ran = random.random()
                if ran > .9:
                    init_board[pos] = 4
                else:
                    init_board[pos] = 2
                count += 1
        self.board = [[init_board[i], init_board[i+1], init_board[i+2], init_board[i+3]] for i in range(0, 13, 4)]

    #print state of board
    def print_board(self):
        print(np.matrix(self.board))

    #generate a new tile on the board
    def generate_piece(self):
        while True:
            x = randint(0,3)
            y = randint(0,3)
            if self.board[x][y] == 0:
                ran = random.random()
                if ran > .9:
                    self.board[x][y] = 4
                else:
                    self.board[x][y] = 2
                break

    #move tile left
    def move_left(self):
        for j in range (len(self.board)):
            row = self.board[j]
            added = set()
            for i in range(3):
                for x in range(i+1, 4):
                    if self.board[j][x] != 0 and self.board[j][x] != self.board[j][i]:
                        break
                    elif self.board[j][i] == self.board[j][x] and self.board[j][i] != 0 and self.board[j][x] != 0 and (j,i) not in added:
                        self.board[j][i] = self.board[j][i]*2
                        self.board[j][x] = 0
                        added.add((j,i))

            zero = []
            full = []
            for k in row:
                if k == 0:
                    zero.append(0)
                else:
                    full.append(k)
            self.board[j] = full + zero

    def move_right(self):
        for j in range (len(self.board)):
            row = self.board[j]
            added = set()
            for i in range(3, 0, -1):
                for x in range(i-1, -1, -1):
                    if self.board[j][x] != 0 and self.board[j][x] != self.board[j][i]:
                        break
                    elif self.board[j][i] == self.board[j][x] and self.board[j][i] != 0 and self.board[j][x] != 0 and (j,i) not in added:
                        self.board[j][i] = self.board[j][i]*2
                        self.board[j][x] = 0
                        added.add((j,i))

            zero = []
            full = []
            for k in row:
                if k == 0:
                    zero.append(0)
                else:
                    full.append(k)
            self.board[j] = zero + full

    def move_board(self, move):
        old_board = deepcopy(self.board)
        if move == 'left':
            self.move_left()
        elif move == 'right':
            self.move_right()
        elif move == 'down':
            self.board = np.transpose(self.board)
            self.move_right()
            self.board = np.transpose(self.board)
        elif move == 'up':
            self.board = np.transpose(self.board)
            self.move_left()
            self.board = np.transpose(self.board)
        isSame = True
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != old_board[i][j]:
                    isSame = False
                    break
        if not isSame:
            self.generate_piece()

    #check how many empty spaces are on the board
    def get_empty(self):
        count = 0
        for x in range(4):
            for y in range(4):
                if self.board[x][y] == 0:
                    count += 1
        return count

    #check if the game has been won/loss
    def check_board(self):
        for i in range(0,4):
            for j in range(0,4):
                if self.board[i][j] == 0:
                    return False
                if i > 0:
                    if self.board[i][j] == self.board[i-1][j]:
                        return False
                if i < 3:
                    if self.board[i][j] == self.board[i+1][j]:
                        return False
                if j > 0:
                    if self.board[i][j] == self.board[i][j-1]:
                        return False
                if j < 3:
                    if self.board[i][j] == self.board[i][j+1]:
                        return False

        return True

    #change the board state
    def set_board(self, board):
        self.board = board

    #retrieve the board state
    def get_board(self):
        return self.board


#play the game
board = Board()
board.print_board()
print()

while True:
    board.print_board()
    move = getch.getch()
    if ord(move) == 27:
        break
    elif move == 'w':
        board.move_board('up')
    elif move == 'a':
        board.move_board('left')
    elif move == 's':
        board.move_board('down')
    elif move == 'd':
        board.move_board('right')
    print()
    if board.check_board():
        board.print_board()
        print("You Lose!")
        break
