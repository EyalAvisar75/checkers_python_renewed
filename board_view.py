import pygame, sys
from pygame.locals import *


class Board:

    def __init__(self):
        self.__board_squares = []
        self.__board_length = 8
        self.__board_width = 8
        self.__square_color1 = 255, 255, 255
        self.__square_color2 = 0, 255, 0
        self.__square_side = 60
        self.__window_surface = pygame.display.set_mode(
            (self.__square_side * self.__board_width
             , self.__square_side * self.__board_length), 0, 32)

    def create_board(self):
        for column in range(self.__board_width):
            self.__board_squares.append([])
            if column % 2 == 0:
                color = self.__square_color2
            else:
                color = self.__square_color1
            for square in range(self.__board_length):
                square_data = {'rect':
                                   pygame.Rect(column * self.__square_side,
                                               square * self.__square_side,
                                               self.__square_side, self.__square_side), 'column': square, 'place': column,
                               'color': color}

                self.__board_squares[column].append(square_data)
                if color == self.__square_color2:
                    color = self.__square_color1
                else:
                    color = self.__square_color2

    def draw_board(self):
        for line in range(self.__board_width):
            for square in range(self.__board_length):
                pygame.draw.rect(self.__window_surface,
                                 self.__board_squares[line][square]['color'],
                                 self.__board_squares[line][square]['rect'])

    def get_board_squares(self):
        return self.__board_squares

    def get_square_side(self):
        return self.__square_side

    def get_square_color1(self):
        return self.__square_color1

    def get_square_color2(self):
        return self.__square_color2

    def get_window_surface(self):
        return self.__window_surface

    def touched_square(self, event):
        side = self.get_square_side()
        square = event.pos[1] // side
        line = event.pos[0] // side
        return square,line

    def reset_color(self):
        for col in range(8):
            for line in range(8):
                if self.__board_squares[col][line]['color'] == (255,0,0) or self.__board_squares[col][line]['color'] == (0,0,255):
                    self.__board_squares[col][line]['color'] = self.__square_color2

    def set_square_color(self, square, color=''):
        if color == '':
            color = 255,0,0
        else:
            color = 0,0,255
        self.__board_squares[square[1]][square[0]]['color'] = color

    def get_square_color(self, square):
        return self.__board_squares[square[1]][square[0]]['color']
