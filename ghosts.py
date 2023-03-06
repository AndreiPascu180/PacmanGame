import pygame as pg
from settings import *
import random
import math
from game import *


class Ghost:
    def __init__(self, gameboard):
        i = random.randrange(4, len(gameboard) - 2)
        j = random.randrange(1, len(gameboard[0]) - 1)
        while gameboard[i][j] == 3 or i > 20:
            i = random.randrange(4, len(gameboard) - 2)
            j = random.randrange(1, len(gameboard[0]) - 1)
        self.row = i
        self.col = j
        self.attacked = False
        self.dir = self.choose_dir(i, j, gameboard)
        self.dead = False
        self.ghostSpeed = 1 / 16
        self.newDir = self.dir
        self.ghostcolor = RED

    @staticmethod
    def canMove(row, col, gameboard):
        if col == -1 or col == len(gameboard[0]):
            return True
        if gameboard[int(row)][int(col)] != 3:
            return True
        return False


    def update_ghost(self, gameboard):
        if self.dead:
            i = random.randrange(4, len(gameboard) - 2)
            j = random.randrange(1, len(gameboard[0]) - 1)
            while gameboard[i][j] != 1 or gameboard[i][j] != 2:
                i = random.randrange(4, len(gameboard) - 2)
                j = random.randrange(1, len(gameboard[0]) - 1)
            self.row = i
            self.col = j
        if self.attacked:
            self.ghostcolor = BLUE
        else:

            self.ghostcolor = RED

        self.newDir = self.checkSurroundings(self.row, self.col, gameboard)

        self.move(gameboard)

    def move(self, gameboard):
        if self.newDir == 0:
            if canMove(math.floor(self.row - self.ghostSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row -= self.ghostSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 1:
            if canMove(self.row, math.ceil(self.col + self.ghostSpeed), gameboard) and self.row % 1.0 == 0:
                self.col += self.ghostSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 2:
            if canMove(math.ceil(self.row + self.ghostSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row += self.ghostSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 3:
            if canMove(self.row, math.floor(self.col - self.ghostSpeed), gameboard) and self.row % 1.0 == 0:
                self.col -= self.ghostSpeed
                self.dir = self.newDir
                return

        if self.dir == 0:
            if canMove(math.floor(self.row - self.ghostSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row -= self.ghostSpeed
        elif self.dir == 1:
            if canMove(self.row, math.ceil(self.col + self.ghostSpeed), gameboard) and self.row % 1.0 == 0:
                self.col += self.ghostSpeed
        elif self.dir == 2:
            if canMove(math.ceil(self.row + self.ghostSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row += self.ghostSpeed
        elif self.dir == 3:
            if canMove(self.row, math.floor(self.col - self.ghostSpeed), gameboard) and self.row % 1.0 == 0:
                self.col -= self.ghostSpeed

    def draw(self):
        if self.ghostcolor == RED:
            ghostImage = pg.image.load(ImagePath + "tile096.png")
        if self.ghostcolor == BLUE:
            ghostImage = pg.image.load(ImagePath + "tile073.png")
        ghostImage = pg.transform.scale(ghostImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))


    def checkSurroundings(self, row, col, gameboard):
        dirs = []
        index = 0
        if col % 1.0 == 0 and row % 1.0 == 0:
            row = math.floor(row)
            col = math.floor(col)
            if self.dir == 0:
                if gameboard[row][col-1] != 3:
                    dirs.append(3)
                    index += 1
                if gameboard[row][col+1] != 3:
                    dirs.append(1)
                    index += 1
                if gameboard[row-1][col] == 3:
                    dirs.append(2)
                    index += 1
            # 0: up, 1: right, 2: down, 3: left
            if self.dir == 1:
                if gameboard[row-1][col] != 3:
                    dirs.append(0)
                    index += 1
                if gameboard[row+1][col] != 3:
                    dirs.append(2)
                    index += 1
                if gameboard[row][col+1] == 3:
                    dirs.append(3)
                    index += 1
            # 0: up, 1: right, 2: down, 3: left
            if self.dir == 2:
                if gameboard[row][col-1] != 3:
                    dirs.append(3)
                    index += 1
                if gameboard[row][col+1] != 3:
                    dirs.append(1)
                    index += 1
                if gameboard[row+1][col] == 3:
                    dirs.append(0)
                    index += 1
            # 0: up, 1: right, 2: down, 3: left
            if self.dir == 3:
                if gameboard[row - 1][col] != 3:
                    dirs.append(0)
                    index += 1
                if gameboard[row + 1][col] != 3:
                    dirs.append(2)
                    index += 1
                if gameboard[row][col - 1] == 3:
                    dirs.append(1)
                    index += 1
            if index > 1:
                choice = random.randrange(0, index)
                return dirs[choice]
        return self.dir

    # 0: up, 1: right, 2: down, 3: left
    @staticmethod
    def choose_dir(row, col, gameboard):
        if gameboard[row-1][col] != 3:
            return 0
        if gameboard[row+1][col] != 3:
            return 2
        if gameboard[row][col-1] != 3:
            return 3
        if gameboard[row][col+1] != 3:
            return 1


