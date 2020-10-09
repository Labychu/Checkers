import pygame
from .board import Board
from .constants import BLACK, WHITE, GREEN, SQUARE_SIZE


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected_piece:
            if not self._move(row, col):
                self.selected_piece = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # noinspection PyAttributeOutsideInit
            self.selected_piece = piece
            # noinspection PyAttributeOutsideInit
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        destination = self.board.get_piece(row, col)
        if self.selected_piece and destination == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    # noinspection PyAttributeOutsideInit
    def change_turn(self):
        # if current turn is for black then change to white, vice versa
        self.turn = WHITE if self.turn == BLACK else BLACK
        self.valid_moves = dict()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            square_center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(self.win, GREEN, square_center, 10)

    def winner(self):
        if self.board.winner() == WHITE:
            return "White"
        elif self.board.winner() == BLACK:
            return "Black"
        else:
            return self.board.winner()
