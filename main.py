import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game
from checkers.board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


def main():
	run = True
	clock = pygame.time.Clock()
	game = Game(WIN)

	# mouse_pos is a tuple
	def get_row_col_from_mouse(mouse_pos):
		x, y = mouse_pos
		mouse_row = y // SQUARE_SIZE
		mouse_col = x // SQUARE_SIZE
		return mouse_row, mouse_col

	while run:
		# clock.tick(FPS)
		if game.winner() is not None:
			print(f"The winner is {game.winner()}!")
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				row, col = get_row_col_from_mouse(pos)
				# send the position of the selected square
				game.select(row, col)
		game.update()
	pygame.quit()


if __name__ == "__main__":
	main()
