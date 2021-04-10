import pygame
import random
from param import *
from board import *
from collections import deque

# -- Sprites --
class Player(pygame.sprite.Sprite):
    def __init__(self, playerNumber, squareNumber, mode , gameBoard):
        pygame.sprite.Sprite.__init__(self)
        self.playerNumber = playerNumber
        self.squareNumber = squareNumber
        self.mode = mode
        if self.mode == 2:
            self.numberOfWalls = 10
        else:
            self.numberOfWalls = 5
        if playerNumber == 1:
            self.image = playerImg1
        elif playerNumber == 2:
            self.image = playerImg2
        elif playerNumber == 3:
            self.image = playerImg3
        elif playerNumber == 4:
            self.image = playerImg4
        self.rect = self.image.get_rect()
        self.rect.x = int(gameBoard[squareNumber].get_rect().x + 8)
        self.rect.y = int(gameBoard[squareNumber].get_rect().y + 8)
        self.draging = False

    def get_square_number(self):
        return self.squareNumber

    def get_num_of_walls(self):
        return self.numberOfWalls

    def set_num_of_walls(self, newNum):
        self.numberOfWalls = newNum

    def set_square_number(self, newSquare, stateBoard):
        oldSquare = self.squareNumber
        stateBoard[oldSquare].set_contaning_beam(False)
        self.squareNumber = newSquare
        stateBoard[newSquare].set_contaning_beam(True)

    def get_player_number(self):
        return self.playerNumber

    def get_player_x(self):
        return int((self.squareNumber) / numberOfRows)

    def get_player_y(self):
        return int((self.squareNumber) % numberOfRows)


class WallSprite(pygame.sprite.Sprite):
    def __init__(self, verticalOrHorizental, numberOfWall, playerNumber, mode):
        pygame.sprite.Sprite.__init__(self)
        self.squareNumber1 = -1
        self.squareNumber2 = -1
        self.squareNumber3 = -1
        self.playerNumber = playerNumber
        self.verticalOrHorizental = verticalOrHorizental
        if verticalOrHorizental == 1:
            self.image = pygame.Surface([int(margin), int(2 * squareSize + margin)])
        elif verticalOrHorizental == 0:
            self.image = pygame.Surface([int(2 * squareSize + margin), int(margin)])
        self.voh = self.verticalOrHorizental
        self.image.fill(wallColor)
        self.rect = self.image.get_rect()
        if mode == 2:
            self.rect.x = 110 + (numberOfWall - 1) * squareSize + (numberOfWall - 2) * margin
        if mode == 4:
            if playerNumber == 1:
                self.rect.x = 238 + (numberOfWall - 1) * (squareSize + margin)
            if playerNumber == 2:
                self.rect.x = 238 + (numberOfWall - 1) * (squareSize + margin)
            if playerNumber == 3:
                self.rect.x = 5
            if playerNumber == 4:
                self.rect.x = 600

        if (playerNumber == 1):
            self.rect.y = 5
        elif (playerNumber == 2):
            self.rect.y = 600
        if (playerNumber == 3):
            self.rect.y = 238 + (numberOfWall - 6) * (squareSize + margin)
        elif (playerNumber == 4):
            self.rect.y = 238 + (numberOfWall - 6) * (squareSize + margin)
        self.initialx = self.rect.x
        self.initialy = self.rect.y

    def get_square_number(self):
        return self.squareNumber1

    def rotate_wall(self, mouse_x, offset_x, mouse_y, offset_y):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = mouse_x + offset_x
        self.rect.y = mouse_y + offset_y
        self.verticalOrHorizental = (self.verticalOrHorizental + 1) % 2

    def set_square_number(self, newSquare, stateBoard):
        stateBoard[self.squareNumber1].set_contaning_beam(False)
        stateBoard[self.squareNumber2].set_contaning_beam(False)
        stateBoard[self.squareNumber3].set_contaning_beam(False)

        if newSquare != -1:
            if self.verticalOrHorizental == 0 and newSquare + 2 <= 288:
                self.squareNumber1 = newSquare
                self.squareNumber2 = newSquare + 1
                self.squareNumber3 = newSquare + 2
            elif self.verticalOrHorizental == 1 and newSquare + 34 <= 288:
                self.squareNumber1 = newSquare
                self.squareNumber2 = newSquare + 17
                self.squareNumber3 = newSquare + 34

            stateBoard[self.squareNumber1].set_contaning_beam(True)
            stateBoard[self.squareNumber2].set_contaning_beam(True)
            stateBoard[self.squareNumber3].set_contaning_beam(True)

        
        else:
            self.squareNumber1 = -1

    def get_voh(self):
        return self.verticalOrHorizental

    def get_x(self):
        return self.initialx

    def get_y(self):
        return self.initialy

    def initial_voh(self):
        return self.voh

    def get_player_number(self):
        return self.playerNumber


class GameState:
    def __init__(self, player1, player2, stateBoard):
        self.player1 = player1
        self.player2 = player2
        self.stateBoard = stateBoard
        self.utilityValue = None
        self.actionToGetHere = None
        self.nextMove = None

    def __hash__(self):
        return hash(tuple(self.stateBoard))

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_state_board(self):
        return self.stateBoard

    def get_utility_value(self):
        return self.utilityValue

    def set_utility_value(self, utilityValue):
        self.utilityValue = utilityValue

    def getNextMove(self):
        return self.nextMove

    def setNextMove(self, move):
        self.nextMove = move