import pygame
from param import *


class Square:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.x = x
        self.y = y
        self.containsBeam = False
        self.squareNumber = x * 17 + y
        self.rect = pygame.Rect(110 + (int(y/2) * (squareSize + margin)), 110 + (int((x/2))* (squareSize + margin)), squareSize, squareSize)
        self.center = (int((y * (squareSize + margin)) + squareSize / 2), int(((x * (squareSize + margin)) + squareSize / 2)))
        self.squareColor = squareDarkerColorColor
    def get_color(self):
        return self.squareColor

    def get_rect(self):
        return self.rect

    def get_number(self):
        return self.squareNumber

    def get_coordinates(self):
        return self.coordinates

    def get_center(self):
        return self.center

    def get_number(self):
        return self.squareNumber

    def get_contaning_beam(self):
        return self.containsBeam

    def set_contaning_beam(self, containsBeam):
        self.containsBeam = containsBeam

    def is_beam_here(self):
        return self.containsBeam

    def set_color(self, color):
        self.squareColor = color

    def set_center(self, center):
        self.center = center

    def is_wall(self):
        return False
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.containsBeam = False
        self.coordinates = (x, y)
        self.wallNumber = x * 17 + y
        if x % 2 == 0 and y % 2 != 0:
            self.rect = pygame.Rect(
                (110 + (int(y / 2 + 1) * squareSize + int(y / 2) * margin), 110 + (int(x / 2) * squareSize + int(x / 2) * margin), margin,
                 squareSize))
        elif x % 2 != 0 and y % 2 == 0:
            self.rect = pygame.Rect(110 + (int(y / 2) * margin + int(y / 2) * squareSize), 110 + (int(x / 2 + 1) * squareSize + int(x / 2) * margin), squareSize, margin)
        elif x % 2 != 0 and y % 2 != 0:
            self.rect = pygame.Rect(110 + (int(y / 2 + 1) * squareSize + int(y / 2) * margin),
                                    110 + (int(x / 2 + 1) * squareSize + int(x / 2) * margin), margin, margin)
        self.color = (backGroundColor)

    def get_number(self):
        return self.wallNumber

    def get_coordinates(self):
        return self.coordinates

    def get_rect(self):
        return self.rect

    def is_wall(self):
        return True

    def get_contaning_beam(self):
        return self.containsBeam

    def set_contaning_beam(self, containsBeam):
        self.containsBeam = containsBeam

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

# -- Board --
def set_board(board):
    for i in range(0, 17):
        for j in range(0, 17):
            if i % 2 == 0 and j % 2 == 0:
                square = Square(i, j)
                board.append(square)
            else:
                wall = Wall(i, j)
                board.append(wall)

def draw_board(board , window):
    for i in range(0, 289):
        pygame.draw.rect(window, board[i].get_color(), board[i].get_rect())