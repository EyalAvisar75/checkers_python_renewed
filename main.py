from board_view import *
from pieces_model import *

# taking pieces in a row unless crowned
# work on lighting relevant allmoves possibilities when board touched
# when taking in a row allow take backward
# logic module better be imported from a different file

class RunGame:
    def __init__(self):
        self.touched = ""
        self.moves = []
        self.all_moves = []
        self.mantype = ""
        self.is_red_turn = True
        # self.is_jump = False
        self.last_move = ""
        self.is_move_completed = True

    def end_game(self):
        pygame.display.quit()
        sys.exit()

    def add_pieces(self, boardview, piecesmodel):
        for index_row in range(8):
            for index_column in range(8):
                if piecesmodel[index_row][index_column]['image'] is not None:
                    boardview.get_window_surface(). \
                        blit(piecesmodel[index_row][index_column]['image'],
                             boardview.get_board_squares()[index_row][index_column]['rect'])

    def check_move(self, square, line, type):
        if type == 'redman black' or type == 'blackman red':
            self.append_king_checked_moves(line, square)
        elif 'redman' == type:
            self.append_redman_checked_move(line, square)
        elif "blackman" == type:
            self.append_blackman_checked_moves(line, square)
        return self.moves

    def append_blackman_checked_moves(self, line, square):
        self.moves = [self.moves[0]]
        self.add_jump_black(square, line)
        if len(self.all_moves) <= 1:
            self.add_advance_black(square, line)

    def append_redman_checked_move(self, line, square):
        self.add_advance_red(square, line)

    def append_king_checked_moves(self, line, square):
        self.append_blackman_checked_moves(line, square)
        self.add_jump_red(square, line)
        if len(self.all_moves) <= 1:
            self.add_advance_red(square, line)

    def offer_move(self, square, line):
        board.reset_color()
        if not self.check_turn(square, line): return []

        self.moves = [(square, line)]
        self.append_offered_moves(line, square)

        is_jumping_offered = False
        if len(self.moves) > 1:
            for move in self.moves:
                line_difference = move[0] - self.moves[0][0]
                if line_difference == 2 or line_difference == -2:
                    is_jumping_offered = True
                    # self.is_jump = True

            if is_jumping_offered:
                self.filter_jumps()
            # if is_jumping_offered and self.is_jump:
            #     print("multi jumps on the way")

            for move in self.moves[1:]:
                board.set_square_color(move)
        return self.moves

    def filter_jumps(self):
        is_filtered = False
        for move in self.moves.copy():
            line_difference = move[0] - self.moves[0][0]
            if line_difference == 1 or line_difference == -1:
                self.moves.remove(move)
                is_filtered = True
        return is_filtered

    def append_offered_moves(self, line, square):
        if 'redman black' in pieces[line][square]['type']:
            self.moves = self.check_move(line, square, 'redman black')
        elif 'blackman red' in pieces[line][square]['type']:
            self.moves = self.check_move(line, square, 'blackman red')
        elif 'redman' in pieces[line][square]['type']:
            self.moves = self.check_move(line, square, 'redman')
        elif 'blackman' in pieces[line][square]['type']:
            self.moves = self.check_move(line, square, 'blackman')

    def check_turn(self, square, line):
        if pieces[line][square]['type'] == "":
            return False

        if self.is_red_turn and 'redman' in pieces[line][square]['type']:
            return True
        if not self.is_red_turn and 'blackman' in pieces[line][square]['type']:
            return True
        output = "black" if 'blackman' in pieces[line][square]['type'] else "red"
        print(output)
        return False

    def confirmed_move(self, move_input):
        if move_input not in self.moves[1:]: return
        if len(self.moves) < 2: return

        self.compute_trajectory(move_input)
        # print("confirmed_move self.is_jump", self.is_jump)
        # if self.is_jump : self.last_move = move_input

        if move_input in self.moves[1:]:
            board.reset_color()
            while len(self.moves) > 0:
                if len(self.moves) == 1:
                    input = self.mantype
                else:
                    input = ''
                if self.mantype == '':
                    self.mantype = piece_model.set_piece(self.moves[0], input)
                else:
                    piece_model.set_piece(self.moves[0], input)

                self.moves.remove(self.moves[0])

            if self.moves == []:
                self.mantype = ""
            return True
        self.moves = []
        self.mantype = ''
        return False

    def change_turn(self):
        self.is_red_turn = not self.is_red_turn
        print(f"turn changed red {self.is_red_turn}")


    def check_game_status(self):
        black_count, red_count = piece_model.count_colors()
        pygame.display.update()
        if black_count == 0:
            print('red won')
            game.end_game()
        if red_count == 0:
            print('black won')
            game.end_game()

    def add_advance_red(self, square, line):
        if 0 < square < 7 and line > 0:
            if pieces[square - 1][line - 1]['type'] == '':
                self.moves.append((line - 1, square - 1))
            if pieces[square + 1][line - 1]['type'] == '':
                self.moves.append((line - 1, square + 1))
        elif square == 7 and line > 0:
            if pieces[square - 1][line - 1]['type'] == '':
                self.moves.append((line - 1, square - 1))
        else:
            if line > 0:
                if pieces[square + 1][line - 1]['type'] == '':
                    self.moves.append((line - 1, square + 1))

    def add_jump_red(self, square, line, type='redman'):
        attacked_piece = 'blackman' if type == 'redman' else 'redman'

        if line < 2: return

        if 1 < square:
            if attacked_piece in pieces[square - 1][line - 1]['type'] \
                    and pieces[square - 2][line - 2]['type'] == "":
                self.all_moves.append((line, square))
                self.all_moves.append((line - 2, square - 2))
        if square < 6:
            if attacked_piece in pieces[square + 1][line - 1]['type'] \
                    and pieces[square + 2][line - 2]['type'] == "":
                self.all_moves.append((line, square))
                self.all_moves.append((line - 2, square + 2))

    def add_advance_black(self, square, line):
        if 0 < square < 7 and line < 7:
            if pieces[square - 1][line + 1]['type'] == '':
                self.moves.append((line + 1, square - 1))
            if pieces[square + 1][line + 1]['type'] == '':
                self.moves.append((line + 1, square + 1))
        elif square == 7 and line < 7:
            if pieces[square - 1][line + 1]['type'] == '':
                self.moves.append((line + 1, square - 1))
        else:
            if line < 7:
                if pieces[square + 1][line + 1]['type'] == '':
                    self.moves.append((line + 1, square + 1))

    def add_jump_black(self, square, line, type="blackman"):
        attacked_piece = 'blackman' if type == 'redman' else 'redman'

        if line > 5: return

        if 1 < square:
            if attacked_piece in pieces[square - 1][line + 1]['type'] \
                    and pieces[square - 2][line + 2]['type'] == "":
                self.all_moves.append((line, square))
                self.all_moves.append((line + 2, square - 2))
        if square < 6:
            if attacked_piece in pieces[square + 1][line + 1]['type'] \
                    and pieces[square + 2][line + 2]['type'] == "":
                self.all_moves.append((line, square))
                self.all_moves.append((line + 2, square + 2))

    def compute_trajectory(self, move_input):
        column_difference = move_input[1] - self.moves[0][1]
        line_difference = move_input[0] - self.moves[0][0]

        if column_difference == 2 or column_difference == -2:
            midsquare_line, midsquare_column = \
                move_input[0] - line_difference // 2, move_input[1] - column_difference // 2
            self.moves = [self.moves[0], (midsquare_line, midsquare_column), move_input]
        else:
            self.moves = [self.moves[0], move_input]

    def check_mandatory_moves(self):
        self.all_moves = []
        for line in range(8):
            for square in range(8):
                piece = pieces[line][square]
                if piece['type'] != "":
                    if self.is_red_turn and "red" in piece['type']:
                        if 'blackman red' in piece['type']:
                            continue
                        self.add_jump_red(line, square)
                        if 'redman black' in piece['type']:
                            self.add_jump_black(line, square, type='redman')
                    if not self.is_red_turn and "black" in piece['type']:
                        if 'redman black' in piece['type']:
                            continue
                        self.add_jump_black(line, square)
                        if 'blackman red' in piece['type']:
                            self.add_jump_red(line, square, type='blackman')



    # def check_continuation_jump(self):
    #     if not game.is_jump: return
    #     print("check_continuation_jump", self.last_move)
    #     # self.is_red_turn = not self.is_red_turn
    #     self.all_moves = []
    #     if self.last_move != "" and len(self.last_move) > 0:
    #         square, row = self.last_move[0], self.last_move[1]
    #     else: return
    #     piece = pieces[square][row]
    #
    #     if 'redman' in piece['type'] and self.is_red_turn:
    #         square, row = piece['position'][0], piece['position'][1]
    #         self.moves = []
    #         self.moves.append((square, row))
    #         self.add_jump_red(square, row)
    #         if len(self.moves) > 1:
    #             self.all_moves += self.moves
    #             print("from square row ", square, row)
    #             print("red all moves", self.all_moves)
    #
    #     elif 'blackman' in piece['type'] and not self.is_red_turn:
    #         square, row = piece['position'][0], piece['position'][1]
    #         self.moves = []
    #         self.moves.append((square, row))
    #         self.add_jump_black(square, row)
    #         if len(self.moves) > 1:
    #             self.all_moves += self.moves
    #             print("from square row ", square, row)
    #             print("black all moves", self.all_moves)


pygame.init()
game = RunGame()
board = Board()
piece_model = Pieces()
pieces = piece_model.get_model()
completed_move = False
board.create_board()


def highlight_mandatory_moves():
    for move in game.all_moves:
        if pieces[move[1]][move[0]]['type'] == "":
            board.set_square_color(move)


while True:
    game.check_game_status()
    for event in pygame.event.get():
        if event.type == QUIT:
            game.end_game()
        if event.type == MOUSEBUTTONUP:
            print("start events moves allmoves", game.moves, game.all_moves)
            if len(game.all_moves) > 1:
                line, square = board.touched_square(event)
                if (line,square) in game.all_moves:
                    index = game.all_moves.index((line,square))
                    if index % 2 == 0:
                        game.moves = [game.all_moves[index],game.all_moves[index+1]]
                    else:
                        game.moves = [game.all_moves[index-1],game.all_moves[index]]

                    if game.confirmed_move((line, square)):
                        game.all_moves = []
                        game.change_turn()
                        print("before events moves allmoves", game.moves, game.all_moves)
                        print("turn changed red", game.is_red_turn)
                    board.reset_color()
            elif game.moves is not None and len(game.moves) > 0:
                print("if allmoves is empty", game.moves, game.all_moves)
                line, square = board.touched_square(event)
                if board.get_square_color((line, square)) == (255,0,0):
                    print("playing", (line, square))
                    if game.confirmed_move((line, square)):
                        game.change_turn()
                        print("turn changed red", game.is_red_turn)
                    board.reset_color()
                else:
                    print("if allmoves empty and pressed nonred square", game.moves, game.all_moves)
                    game.moves = game.offer_move(line, square)
            else:
                print("if moves, allmoves are empty", game.moves, game.all_moves)
                line, square = board.touched_square(event)
                piece_model.get_piece((line,square))
                game.touched = line,square
                print("touched", line, square)
                game.check_mandatory_moves()
                print("all moves after mandatory_move", game.all_moves)
                # game.all_moves = []
                if game.all_moves == []:
                    print("mandatory returned [] moves allmoves", game.moves, game.all_moves)
                    game.moves = game.offer_move(line, square)
                else:
                    print("allmoves not empty moves allmoves", game.moves, game.all_moves)
                    highlight_mandatory_moves()


    board.draw_board()
    game.add_pieces(board, pieces)
    completed_move = False
    pygame.display.update()
