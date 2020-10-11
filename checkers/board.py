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

	# Initiate the 2d list board
	# 0 -> blank square
	# a Piece object -> a piece exists on that square
	def create_board(self):
		for row in range(ROWS):
			# append a blank row
			self.board.append([])
			for col in range(COLS):
				# A feature of checkers: all pieces are on dark squares
				# E.g row 0: pieces can be on col 1 - 3 - 5 - 7 etc
				if col % 2 == (row + 1) % 2:
					# Only the first and last rows have pieces initially
					# If satisfy the condition -> append a Piece obj to the current row
					# Otherwise append 0 to the row
					if row < 3:
						self.board[row].append(Piece(row, col, WHITE))
					elif row > ROWS - 4:
						self.board[row].append(Piece(row, col, BLACK))
					else:
						self.board[row].append(0)
				else:
					self.board[row].append(0)

	# Return either a Piece obj or a 0
	def get_piece(self, row, col):
		return self.board[row][col]

	# move the selected piece to a square by swapping content
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

	# Display the board on the given surface
	def draw(self, win):
		# First draw the squares
		# On each (row, col) if there is a piece then draw it
		draw_squares(win)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.get_piece(row, col)
				if piece != 0:
					piece.draw(win)

	# return all the valid moves of the given piece
	# a move is a list contain
	def get_valid_moves(self, piece):
		# the dict stores all available moves for the selected piece
		moves = dict()
		left_col = piece.col - 1
		right_col = piece.col + 1
		row = piece.row
		# Try to traverse down left and down right for White, up left and up right for Black, a king can do both
		# When meet the end return all the valid moves until then into the moves dict
		if piece.color == BLACK or piece.king:
			moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left_col, []))
			moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right_col, []))
		if piece.color == WHITE or piece.king:
			moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left_col, []))
			moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right_col, []))

		return moves

	# _traverse_left has 6 parameters exclude self
	# start, stop are the next row and the row after destination row.
	# Stop must not be outside of board. Also stop max is current row +- 3 (in case the piece hop through st)
	# step takes either 1 or -1, 1 for moving downward, -1 for moving upward
	# color: piece_color
	# left_col: column to the left of the piece
	# skipped: the list of square that the piece hop over, aka the list of the other color pieces ...
	# that the selected piece defeated
	def _traverse_left(self, start, stop, step, color, left_col, skipped):
		moves = dict()  # the valid moves that this method returns
		last = list()  # all the squares that the piece moves through during the traverse
		for r in range(start, stop, step):
			if left_col < 0:  # if out of bound
				break
			des_piece = self.get_piece(r, left_col)  # get the the piece at the square we traverse to
			if des_piece == 0:
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
			elif des_piece.color == color:
				break
			else:
				last = [des_piece]
			left_col -= 1

		return moves

	# _traverse_right has 6 parameters exclude self
	# start, stop are the next row and the row after destination row.
	# Stop must not be outside of board. Also stop max is current row +- 3 (in case the piece hop through st)
	# step takes either 1 or -1, 1 for moving downward, -1 for moving upward
	# color: piece_color
	# right_col: column to the right of the piece
	# skipped: the list of square that the piece hop over, aka the list of the other color pieces ...
	# that the selected piece defeated
	def _traverse_right(self, start, stop, step, color, right_col, skipped):
		moves = dict()  # the valid moves that this method returns
		last = list()  # all the squares that the piece moves through during the traverse
		for r in range(start, stop, step):
			if right_col >= COLS:  # if out of bound
				break
			des_piece = self.get_piece(r, right_col)
			if des_piece == 0:
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
			elif des_piece.color == color:
				break
			else:
				last = [des_piece]
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

