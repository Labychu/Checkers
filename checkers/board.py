import pygame
from .piece import Piece
from .constants import CLR1, CLR2, BG, ROWS, COLS, SQUARE_SIZE, BLACK, WHITE


def draw_squares(win):
	win.fill(BG)
	for row in range(ROWS):
		for col in range(row % 2, ROWS, 2):
			pygame.draw.rect(win, CLR1, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		for col in range((row+1) % 2, COLS, 2):
			pygame.draw.rect(win, CLR2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


class Board:
	def __init__(self):
		# list of pieces on the board
		# squares with no pieces is represented as 0
		# else represented as a Piece object
		self.board = []
		self.selected_piece = None
		self.red_left = self.white_left = 12
		self.red_kings = self.white_kings = 0
		self.create_board()

	def create_board(self):
		for row in range(ROWS):
			self.board.append([])
			for col in range(COLS):
				if col % 2 == (row + 1) % 2:
					if row < 3:
						self.board[row].append(Piece(row, col, WHITE))
					elif row > ROWS - 4:
						self.board[row].append(Piece(row, col, BLACK))
					else:
						self.board[row].append(0)
				else:
					self.board[row].append(0)

	def draw(self, win):
		draw_squares(win)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.board[row][col]
				if piece != 0:
					piece.draw(win)
