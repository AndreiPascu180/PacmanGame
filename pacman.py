from game import *
import math
from settings import *
import pygame

class PacmanCharacter:
    def __init__(self, row, col, game):
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1 / 8
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 0  # 0: North, 1: East, 2: South, 3: West
        self.newDir = 0
        self.game = game

    def update(self, gameboard):
        if self.newDir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed), gameboard) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed), gameboard) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed
                self.dir = self.newDir
                return

        if self.dir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
        elif self.dir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed), gameboard) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
        elif self.dir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col, gameboard) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
        elif self.dir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed), gameboard) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed

    def draw(self):
        if self.game.paused:
            pacmanImage = pygame.image.load(ImagePath + "tile112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage,
                        (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))
            return

        if self.mouthChangeCount == self.mouthChangeDelay:
            self.mouthChangeCount = 0
            self.mouthOpen = not self.mouthOpen
        self.mouthChangeCount += 1
        if self.dir == 0:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ImagePath + "tile049.png")
            else:
                pacmanImage = pygame.image.load(ImagePath + "tile051.png")
        elif self.dir == 1:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ImagePath + "tile052.png")
            else:
                pacmanImage = pygame.image.load(ImagePath + "tile054.png")
        elif self.dir == 2:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ImagePath + "tile053.png")
            else:
                pacmanImage = pygame.image.load(ImagePath + "tile055.png")
        elif self.dir == 3:
            if self.mouthOpen:
                pacmanImage = pygame.image.load(ImagePath + "tile048.png")
            else:
                pacmanImage = pygame.image.load(ImagePath + "tile050.png")

        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))


def canMove(row, col, gameboard):
    if col == -1 or col == len(gameboard[0]):
        return True
    if gameboard[int(row)][int(col)] != 3:
        return True
    return False
