# Project - Conway's Game of Life
# Functions to support main module
# Michael Xu
# May 19, 2020


# import pygame module for graphical user interface
import pygame

# pygame setup
pygame.init()
win = pygame.display.set_mode(flags=pygame.FULLSCREEN)
win.fill((230, 230, 230))
pygame.display.update()
pygame.display.set_caption("Conway's Game of Life")
screen_width, screen_height = pygame.display.get_surface().get_size()


def alive(grid, coordinate):
	"""
    Determines whether a cell is alive or not.

    Args:
        grid (matrix): two dimensional list containing all cells.
        coordinate (tuple): (x, y) coordinate of one cell.

    Returns:
        bool: True if the value of the cell is 1, False otherwise.

    Example:
        >>> alive([[0, 1, 1], [0, 0, 1], [1, 0, 1]], (1, 2))
        True
        >>> alive([[0, 1, 1], [0, 0, 1], [1, 0, 1]], (1, 1))
        False
    """
	
	# make a copy of grid parameter to not change original grid
	temp_grid = grid.copy()
	
	# process coordinate
	x, y = coordinate[0] + 1, coordinate[1] + 1

	# add buffer around matrix to avoid IndexError when referencing cells around the edges
	temp_grid.insert(0, [0] * len(temp_grid[0]))
	temp_grid.append([0] * len(temp_grid[0]))
	for i in range(len(temp_grid)):
		row_ = temp_grid[i].copy()
		row_.insert(0, 0)
		row_.append(0)
		temp_grid[i] = row_

	# count number of alive neighbours
	cell = temp_grid[y][x]
	count = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			if i == 0 and j == 0:
				continue
			else:
				if temp_grid[y + i][x + j] == 1:
					count += 1

	# return alive or dead according to conway's game of life rules
	if cell == 0:
		if count == 3:
			return True
	else:
		if count == 2 or count == 3:
			return True
	return False


def input_grid(matrix_width, matrix_height):
	"""
    Uses pygame to input a user-created grid.

    Args:
        matrix_width (int): width of matrix
        matrix_height (int): height of matrix

    Returns:
        matrix: user-created matrix containing 1 and 0's

    Example:
        >>> input_grid(3, 3)
        [[0, 1, 1], [0, 0, 1], [1, 0, 1]]
    """
	
	# clear screen
	pygame.draw.rect(win, (230, 230, 230), (0, 0, screen_width, screen_height))
	
	# create a temporary grid containing 2's in order to draw an empty grid
	temp_grid = [[2 for j in range(matrix_width)] for i in range(matrix_height)]
	
	# calculate grid height, cell size, and grid width with arguments
	if matrix_height >= matrix_width:
		grid_height = screen_height - 200
		cell_size = int(grid_height / matrix_height)
		grid_width = cell_size * matrix_width
	else:
		grid_width = screen_width - 200
		cell_size = int(grid_width / matrix_width)
		grid_height = cell_size * matrix_height

	# display instructions below grid
	arial_40 = pygame.font.SysFont("Arial", 40)
	text = arial_40.render(f"The Yellow cell is the currently selected. Press 1 for alive or 0 for dead.", True, (0, 0, 0))
	win.blit(text, (screen_width / 2 - 470, screen_height - 60))

	# draw a grid with all cells filled in with white
	for row in range(len(temp_grid)):
		for col in range(len(temp_grid[row])):
			pygame.draw.rect(win, (255, 255, 255), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
			pygame.draw.rect(win, (0, 0, 0), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size), 1)
	pygame.display.update()
	
	# create a new matrix
	real_grid = []

	# input user choice of alive or dead for each cell in the grid
	for row in range(len(temp_grid)):
		real_row = []
		for col in range(len(temp_grid[row])):
			
			# draw selected cell filled in with yellow 
			pygame.draw.rect(win, (245, 209, 66), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
			pygame.draw.rect(win, (0, 0, 0), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size), 1)
			pygame.display.update()
			
			# receive user input
			while True:
				pygame.event.get()
				pygame.time.delay(100)
				keys = pygame.key.get_pressed()
				
				# redraw selected cell filled in with green if the cell is alive
				if keys[pygame.K_1]:
					real_row.append(1)
					pygame.draw.rect(win, (63, 235, 63), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
					break

				# redraw selected cell filled in with red if the cell is dead
				if keys[pygame.K_0]:
					real_row.append(0)
					pygame.draw.rect(win, (255, 54, 54), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
					break
			
			# draw border around cell
			pygame.draw.rect(win, (0, 0, 0), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size), 1)
		real_grid.append(real_row)
	return real_grid


def draw_grid(grid, generation, mode):
	"""
    Uses pygame to display a grid.

    Args:
        grid (matrix): matrix to be displayed.
        generation (int): current generation of simulation.
        mode (int): method of proceeding to next generation (1 if manual, 0 if automatic).

    Returns:
        None

    Example:
        >>> draw_grid([[0, 1, 1], [0, 0, 1], [1, 0, 1]], 5, 1)
    """
	
	# clear screen
	pygame.draw.rect(win, (230, 230, 230), (0, 0, screen_width, screen_height))
	
	# calculate matrix height and width
	matrix_height = len(grid)
	matrix_width = len(grid[0])

	# calculate grid height, cell size, and grid width
	if matrix_height >= matrix_width:
		grid_height = screen_height - 200
		cell_size = int(grid_height / matrix_height)
		grid_width = cell_size * matrix_width
	else:
		grid_width = screen_width - 200
		cell_size = int(grid_width / matrix_width)
		grid_height = cell_size * matrix_height
		
	# generate font with pygame
	arial_40 = pygame.font.SysFont("Arial", 40)

	# display instructions below grid if method of proceeding to next generation is manual
	if mode == 1:
		text = arial_40.render(f"Press ENTER to proceed to the next generation", True, (0, 0, 0))
		win.blit(text, (screen_width / 2 - 315, screen_height - 60))

	# display generation number above grid
	text = arial_40.render(f"Generation: {generation}", True, (0, 0, 0))
	win.blit(text, (screen_width / 2 - 110, 40))

	# draw each cell in the grid
	for row in range(len(grid)):
		for col in range(len(grid[row])):

			# draw cell filled in with green if cell is a 1 (alive)
			if grid[row][col] == 1:
				pygame.draw.rect(win, (63, 235, 63), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
				pygame.draw.rect(win, (0, 0, 0), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size), 1)

			# draw cell filled in with red if cell is a 0 (dead)
			else:
				pygame.draw.rect(win, (255, 54, 54), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size))
				pygame.draw.rect(win, (0, 0, 0), (int((screen_width - grid_width) / 2 + cell_size * col), int((screen_height - grid_height) / 2 + cell_size * row), cell_size, cell_size), 1)

	# update pygame display
	pygame.display.update()
	
	
def main_screen():
	"""
	Uses pygame to display main screen with title, creator, and instructions.
	"""

	# display game title
	arial_80 = pygame.font.SysFont("Arial", 80)
	text = arial_80.render("Conway's Game of Life!", True, (0, 0, 0), (230, 230, 230))
	win.blit(text, (screen_width / 2 - 320, 200))

	# display creator
	arial_40 = pygame.font.SysFont("Arial", 40)
	text = arial_40.render("By Michael Xu", True, (0, 0, 0), (230, 230, 230))
	win.blit(text, (screen_width / 2 - 110, 300))

	# display instructions
	arial_40 = pygame.font.SysFont("Arial", 40)
	text = arial_40.render("Please return to terminal", True, (255, 54, 54), (230, 230, 230))
	win.blit(text, (screen_width / 2 - 175, 500))

	# update pygame display
	pygame.display.update()
