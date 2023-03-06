import sys
import pygame as pg
from settings import *
from pacman import *
import random
from ghosts import *

pg.init()

pg.display.set_caption("Pacman")
logo = pg.image.load(ImagePath + 'logo.png')
pg.display.set_icon(logo)


class Game:

    def __init__(self, level, score):
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'start'
        self.level = level
        self.score = score
        self.paused = True
        self.pacman = PacmanCharacter(26.0, 13.5, self)
        self.pacmanUpdateDelay = 1
        self.pacmanUpdateCount = 0
        self.berryEaten = False
        self.time_eaten = 0
        self.powerTime = 5000
        self.ghosts = [Ghost(gameboard1), Ghost(gameboard1), Ghost(gameboard1), Ghost(gameboard1)]
        self.ghostScore = 200
        self.gameOver = False

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            if self.state == 'start':
                self.start_events()
                self.start_draw()

            if self.state == 'playing':
                self.playing_events()
                if self.level == 1:
                    self.playing_update(gameboard1)
                if self.level == 2:
                    self.playing_update(gameboard2)
                if self.level == 3:
                    self.playing_update(gameboard3)
                if self.level == 1:
                    self.playing_draw(gameboard1)
                if self.level == 2:
                    self.playing_draw(gameboard2)
                if self.level == 3:
                    self.playing_draw(gameboard3)

        pg.quit()
        sys.exit()

    ####################### Help Functions #######################

    def draw_text(self, screen, text, pos, size, color, font):
        font = pg.font.SysFont(font, size)
        to_print = font.render(text, False, color)
        text_size = to_print.get_size()
        pos[0] = pos[0] - text_size[0] // 2
        pos[1] = pos[1] - text_size[1] // 2
        screen.blit(to_print, pos)

    def touchingPacman(self, row, col):
        if row - 0.5 <= self.pacman.row <= row and col == self.pacman.col:
            return True
        elif row + 0.5 >= self.pacman.row >= row and col == self.pacman.col:
            return True
        elif row == self.pacman.row and col - 0.5 <= self.pacman.col <= col:
            return True
        elif row == self.pacman.row and col + 0.5 >= self.pacman.col >= col:
            return True
        elif row == self.pacman.row and col == self.pacman.col:
            return True
        return False

    ####################### 1 Time functions #######################

    def start_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.state = 'playing'

    def start_draw(self):
        screen.fill((0, 0, 0))
        self.draw_text(screen, 'PRESS ENTER TO BEGIN', [WIDTH // 2, HEIGHT // 2 - 50],
                       START_TEXT_SIZE, YELLOW, START_FONT)
        self.draw_text(screen, 'LEVEL: 1', [46, 10], 16, WHITE, START_FONT)
        pg.display.update()

    ###################### Playing Functions #######################

    def playing_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if not self.paused:
                    self.paused = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.running = False
                if event.key == pg.K_UP:
                    if not self.paused:
                        self.pacman.newDir = 0
                elif event.key == pg.K_RIGHT:
                    if not self.paused:
                        self.pacman.newDir = 1
                elif event.key == pg.K_DOWN:
                    if not self.paused:
                        self.pacman.newDir = 2
                elif event.key == pg.K_LEFT:
                    if not self.paused:
                        self.pacman.newDir = 3
                elif event.key == pg.K_w:
                    if not self.paused:
                        self.FPS += 7
                elif event.key == pg.K_s:
                    if not self.paused:
                        self.FPS -= 7
                elif event.key == pg.K_f:
                    if not self.paused:
                        self.FPS = 60

    def playing_update(self, gameboard):

        if self.check_win(gameboard):
            if self.level == 3:
                self.gameOver = True
                while self.gameOver:
                    self.draw_text(screen, 'YOU WIN, Congrats!! Press Q to Quit', [WIDTH // 2, HEIGHT // 2],
                                   START_TEXT_SIZE + 8, YELLOW, START_FONT)
                    for x in pg.event.get():
                        if x.type == pg.QUIT:
                            self.gameOver = False
                            self.running = False
                        if x.type == pg.KEYDOWN and x.key == pg.K_q:
                            self.gameOver = False
                            self.running = False
                    pygame.display.update()
                return
            else:
                self.level += 1
                self.paused = True
                if self.level == 2:
                    self.reset(gameboard2)
                if self.level == 3:
                    self.reset(gameboard3)
                return

        # Updating Score
        self.pacmanUpdateCount += 1
        if self.pacmanUpdateCount == self.pacmanUpdateDelay:
            self.pacmanUpdateCount = 0
            self.pacman.update(gameboard)
            self.pacman.col %= len(gameboard[0])
            if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
                if gameboard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                    gameboard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    self.score += 10
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                # Eats berry
                elif gameboard[int(self.pacman.row)][int(self.pacman.col)] == 5:
                    self.berryEaten = True
                    self.time_eaten = pygame.time.get_ticks()
                    gameboard[int(self.pacman.row)][int(self.pacman.col)] = 1
                    i = random.randrange(1, len(gameboard) - 2)
                    j = random.randrange(1, len(gameboard[0]))
                    while gameboard[i][j] != 1:
                        i = random.randrange(1, len(gameboard) - 2)
                        j = random.randrange(1, len(gameboard[0]))
                    gameboard[i][j] = 5
                    pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                    self.score += 50

        time = pygame.time.get_ticks()

        if time - self.time_eaten > self.powerTime:
            self.berryEaten = False
        for ghost in self.ghosts:
            if self.berryEaten:
                ghost.attacked = True
            else:
                ghost.attacked = False
            if self.level == 1:
                ghost.update_ghost(gameboard1)
            if self.level == 2:
                ghost.update_ghost(gameboard2)
            if self.level == 3:
                ghost.update_ghost(gameboard3)

            # Touches ghost and dies
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                self.gameOver = True
                while self.gameOver:
                    self.draw_text(screen, 'YOU LOSE, Press Q to quit the game', [WIDTH // 2, HEIGHT//2],
                           START_TEXT_SIZE + 10, RED, START_FONT)
                    for x in pg.event.get():
                        if x.type == pg.QUIT:
                            self.gameOver = False
                            self.running = False
                        if x.type == pg.KEYDOWN and x.key == pg.K_q:
                            self.gameOver = False
                            self.running = False
                    pygame.display.update()
                return

            # Eats ghost
            elif self.touchingPacman(ghost.row, ghost.col) and ghost.attacked:
                self.score += self.ghostScore
                i = random.randrange(4, len(gameboard) - 2)
                j = random.randrange(1, len(gameboard[0]))
                while gameboard[i][j] == 3 or gameboard[i][j] == 5:
                    i = random.randrange(4, len(gameboard) - 2)
                    j = random.randrange(1, len(gameboard[0]))
                ghost.row = i
                ghost.col = j
                if self.level == 1:
                    ghost.update_ghost(gameboard1)
                if self.level == 2:
                    ghost.update_ghost(gameboard2)
                if self.level == 3:
                    ghost.update_ghost(gameboard3)






    def playing_draw(self, gameboard):
        screen.fill((0, 0, 0))

        # DRAW LEVEL

        self.draw_text(screen, 'LEVEL: ', [40, 10], 16, WHITE, START_FONT)
        if self.level == 1:
            self.draw_text(screen, '1', [76, 10], 16, WHITE, START_FONT)
        elif self.level == 2:
            self.draw_text(screen, '2', [76, 10], 16, WHITE, START_FONT)
        elif self.level == 3:
            self.draw_text(screen, '3', [76, 10], 16, WHITE, START_FONT)

        # DRAW SCORE
        self.draw_text(screen, 'SCORE:', [WIDTH - 100, 10], 16, WHITE, START_FONT)
        self.draw_text(screen, str(self.score), [WIDTH - 35, 10], 16, WHITE, START_FONT)

        # DRAW LABYRINTH
        for i in range(3, len(gameboard) - 2):
            for j in range(len(gameboard[0])):
                if gameboard[i][j] == 3:  # Draw wall
                    pg.draw.rect(screen, (0, 0, 255),
                                 (j * square, i * square, square, square))
                elif gameboard[i][j] == 2:  # Draw Tic-Tak
                    pg.draw.circle(screen, GREY, (j * square + square // 2, i * square + square // 2),
                                   square // 6)
                elif gameboard[i][j] == 5:
                    pg.draw.circle(screen, GREEN, (j * square + square // 2, i * square + square // 2),
                                   square // 3)

        # DRAW PACMAN
        self.pacman.draw()

        # DRAW GHOSTS
        for ghost in self.ghosts:
            ghost.draw()

        # CHECK PAUSE
        while self.paused:
            self.draw_text(screen, 'PAUSED, PRESS SPACE TO CONTINUE', [WIDTH // 2, 35],
                           START_TEXT_SIZE, (255, 255, 255), START_FONT)
            for x in pg.event.get():
                if x.type == pg.QUIT:
                    self.paused = False
                    self.running = False
                if x.type == pg.KEYDOWN and x.key == pg.K_SPACE:
                    self.paused = False
            self.pacman.draw()
            pg.display.update()

        pg.display.update()

    # CHECK WIN
    def check_win(self, gameboard):
        win = 1
        for i in range(1, len(gameboard) - 1):
            for j in range(1, len(gameboard[0]) - 1):
                if gameboard[i][j] == 2:
                    win = 0
        return win

    def reset(self, gameboard):
        self.pacman.row = 26.0
        self.pacman.col = 13.5
        for ghost in self.ghosts:
            i = random.randrange(4, len(gameboard) - 2)
            j = random.randrange(1, len(gameboard[0]) - 1)
            while gameboard[i][j] == 3 or i > 22:
                i = random.randrange(4, len(gameboard) - 2)
                j = random.randrange(1, len(gameboard[0]) - 1)
            ghost.row = i
            ghost.col = j

