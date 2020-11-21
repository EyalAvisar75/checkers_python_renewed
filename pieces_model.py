import pygame

#strong coupling to checkers,
# start position and images should be in a file
# variables names should be changed accordingly


class Pieces:
    def __init__(self):
        self.__pieces = []
        for row in range(8):
            self.__pieces.append([])
            for piece in range(8):
                self.__pieces[row].append({'image': None, 'position': [], 'type': ""})

        for row in range(0,8,2):
            for square in range(3):
                if square == 1:
                    row += 1
                if square == 2:
                    row -= 1
                piece = {'image': None, 'position': [row,square], 'type': 'blackman'}
                piece['image'] = pygame.image.load('venv/resources/black_piece.png')
                piece['image'] = pygame.transform.scale(piece['image'],
                                                    (60, 60))
                self.__pieces[row][square] = piece

        for row in range(1,8,2):
            for square in range(5,8,1):
                if square == 6:
                    row -= 1
                if square == 7:
                    row += 1
                piece = {'image': None, 'position': [row, square], 'type': 'redman'}
                piece['image'] = pygame.image.load('venv/resources/red_piece.png')
                piece['image'] = pygame.transform.scale(piece['image'],
                                                    (60, 60))
                self.__pieces[row][square] = piece

    def get_model(self):
        return self.__pieces

    def set_piece(self, square, mantype):
        if self.__pieces[square[1]][square[0]]['position'] == []:
            piece = self.__pieces[square[1]][square[0]]
            piece['position'] = [square[1], square[0]]
            if mantype == 'redman':
                piece['image'] = pygame.image.load('venv/resources/red_piece.png')
            elif mantype == 'blackman':
                piece['image'] = pygame.image.load('venv/resources/black_piece.png')
            elif mantype == 'redman black':
                piece['image'] = pygame.image.load('venv/resources/red_king.png')
            elif mantype == 'blackman red':
                piece['image'] = pygame.image.load('venv/resources/black_king.png')
            if piece['image'] is not None:
                piece['image'] = pygame.transform.scale(piece['image'],
                                                    (60, 60))
            piece['type'] = mantype
        else:
            if mantype == '':
                mantype = self.__pieces[square[1]][square[0]]['type']
            self.__pieces[square[1]][square[0]]['position'] = []
            self.__pieces[square[1]][square[0]]['image'] = None
            self.__pieces[square[1]][square[0]]['type'] = ""
            return mantype

    def get_piece(self, square):
        print("returning piece in ", square)
        print(self.__pieces[square[1]][square[0]]['position'])
        print(self.__pieces[square[1]][square[0]]['type'])


    def count_colors(self):
        black_count = 0
        red_count = 0

        for row in range(8):
            for column in range(8):
                if 'blackman' in self.__pieces[row][column]['type']:
                    if column == 7:
                        self.crown(self.__pieces[row][column])
                    black_count += 1
                elif 'redman' in self.__pieces[row][column]['type']:
                    if column == 0:
                        self.crown(self.__pieces[row][column])
                    red_count += 1

        return (black_count, red_count)

    def crown(self, piece):
        if piece['type'] == 'blackman':
            piece['type'] = 'blackman red'
            piece['image'] = pygame.image.load('venv/resources/black_king.png')
            piece['image'] = pygame.transform.scale(piece['image'],
                                                    (60, 60))
        if piece['type'] == 'redman':
            piece['type'] = 'redman black'
            piece['image'] = pygame.image.load('venv/resources/red_king.png')
            piece['image'] = pygame.transform.scale(piece['image'],
                                                    (60, 60))
