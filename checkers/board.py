import pygame
from .constants import CLR1, CLR2, BG, ROWS, SQUARE_SIZE


class Board:
	def __init__(self):
		self.board = []
		self.selected_piece = None
		self.red_left = self.white_left = 12
		self.red_kings = self.white_kings = 0

	def draw_squares(self, win):
		win.fill(BG)
		for row in range(ROWS):
			for col in range (row % 2, ROWS, 2):
				pygame.draw.rect(win, CLR1, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			for col in range ((row+1) % 2, ROWS, 2):
				pygame.draw.rect(win, CLR2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

