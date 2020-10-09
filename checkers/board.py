import pygame
from .piece import Piece
from .constants import CLR1, CLR2, GREEN, ROWS, COLS, SQUARE_SIZE, BLACK, WHITE


def draw_squares(win):
	win.fill(GREEN)
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
		self.black_left = self.white_left = 12
		self.black_kings = self.white_kings = 0
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

	def get_piece(self, row, col):
		return self.board[row][col]

	def move(self, piece, row, col):
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)
		if row == ROWS - 1 or row == 0:
			if piece.king:
				return
			piece.make_king()
			if piece.color == WHITE:
				self.white_kings += 1
			elif piece.color == BLACK:
				self.black_kings += 1

	def draw(self, win):
		draw_squares(win)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.get_piece(row, col)
				if piece != 0:
					piece.draw(win)

	def get_valid_moves(self, piece):
		moves = dict()
		left_col = piece.col - 1
		right_col = piece.col + 1
		row = piece.row

		if piece.color == BLACK or piece.king:
			moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left_col, []))
			moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right_col, []))
		if piece.color == WHITE or piece.king:
			moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left_col, []))
			moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right_col, []))

		return moves

	def _traverse_left(self, start, stop, step, color, left_col, skipped):
		moves = dict()
		last = list()
		for r in range(start, stop, step):
			if left_col < 0:
				break
			current_piece = self.get_piece(r, left_col)
			if current_piece == 0:
				if skipped and not last:
					break
				elif skipped:
					moves[(r, left_col)] = last + skipped
				else:
					moves[(r, left_col)] = last

				if last:
					if step == -1:
						row = max(r - 3, 0)
					else:
						row = min(r + 3, ROWS)

					moves.update(self._traverse_left(r + step, row, step, color, left_col - 1, skipped=last))
					moves.update(self._traverse_right(r + step, row, step, color, left_col + 1, skipped=last))
				break
			elif current_piece.color == color:
				break
			else:
				last = [current_piece]
			left_col -= 1

		return moves

	def _traverse_right(self, start, stop, step, color, right_col, skipped):
		moves = dict()
		last = list()
		for r in range(start, stop, step):
			if right_col >= COLS:
				break
			current_piece = self.get_piece(r, right_col)
			if current_piece == 0:
				if skipped and not last:
					break
				elif skipped:
					moves[(r, right_col)] = last + skipped
				else:
					moves[(r, right_col)] = last

				if last:
					if step == -1:
						row = max(r - 3, -1)
					else:
						row = min(r + 3, ROWS)

					moves.update(self._traverse_left(r + step, row, step, color, right_col - 1, skipped=last))
					moves.update(self._traverse_right(r + step, row, step, color, right_col + 1, skipped=last))
				break
			elif current_piece.color == color:
				break
			else:
				last = [current_piece]
			right_col += 1

		return moves

	def remove(self, pieces):
		for piece in pieces:
			self.board[piece.row][piece.col] = 0
			if piece == 0:
				continue
			if piece.color == BLACK:
				self.black_left -= 1
				if piece.king:
					self.black_kings -= 1
			else:
				self.white_left -= 1
				if piece.king:
					self.black_kings -= 1

	def winner(self):
		if self.black_left <= 0:
			return WHITE
		if self.white_left <= 0:
			return BLACK
		return None

