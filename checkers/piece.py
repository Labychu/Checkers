import pygame
from .constants import BLACK, WHITE, SQUARE_SIZE


class Piece:
	PADDING = 10
	OUTLINE = 2

	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.king = False

		self.direction = 1 if self.color == WHITE else -1

		self.x = 0
		self.y = 0
		self.calc_pos()

	def calc_pos(self):
		self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
		self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

	def make_king(self):
		self.king = True

	def draw(self, win):
		radius = SQUARE_SIZE // 2 - self.PADDING
		outline_color = BLACK if self.color == WHITE else WHITE
		pygame.draw.circle(win, outline_color, (self.x, self.y), radius + self.OUTLINE)
		pygame.draw.circle(win, self.color, (self.x, self.y), radius)

	def __repr__(self):
		return str(self.color)

