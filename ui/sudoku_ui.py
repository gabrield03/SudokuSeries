import pygame
from sys import exit
from pathlib import Path
#from sudoku import draw_initial_board


pygame.init()

window = pygame.display.set_mode((800, 800))
window.fill('white')
pygame.display.set_caption('Sudoku')


# Controlling the frame rate
clock = pygame.time.Clock()

# Thick borders
border_horizontal_dark = pygame.Surface((650, 2))
border_horizontal_dark.fill('black')

border_vertical_dark = pygame.Surface((2, 650))
border_vertical_dark.fill('black')

grid_size = 9
cell_size = 72

offset_x_y = 75
border_offset = 1

offset = offset_x_y + border_offset

# Load and create the numbers
base_dir = Path(__file__).resolve().parent.parent # Path to SudokuSeries

assets_dir = base_dir / 'assets' # Path to assets


# Transform the number png's to the correct size
def transform_png(surf):
    surf = pygame.transform.scale(
    surf,
    (int(surf.get_width() * (30 / surf.get_height())), 30))

    return surf

num_surf_1 = pygame.image.load(assets_dir / 'roboto_font_number_1.png').convert_alpha()
num_surf_1 = transform_png(num_surf_1)
num_rect_1 = num_surf_1.get_rect(midbottom = (0, 200))

num_surf_2 = pygame.image.load(assets_dir / 'roboto_font_number_2.png').convert_alpha()
num_surf_2 = transform_png(num_surf_2)
num_rect_2 = num_surf_2.get_rect(midbottom = (80, 200))

num_surf_3 = pygame.image.load(assets_dir / 'roboto_font_number_3.png').convert_alpha()
num_surf_3 = transform_png(num_surf_3)
num_rect_3 = num_surf_3.get_rect(midbottom = (180, 200))

num_surf_4 = pygame.image.load(assets_dir / 'roboto_font_number_4.png').convert_alpha()
num_surf_4 = transform_png(num_surf_4)
num_rect_4 = num_surf_4.get_rect(midbottom = (280, 200))

num_surf_5 = pygame.image.load(assets_dir / 'roboto_font_number_5.png').convert_alpha()
num_surf_5 = transform_png(num_surf_5)
num_rect_5 = num_surf_5.get_rect(midbottom = (380, 200))

num_surf_6 = pygame.image.load(assets_dir / 'roboto_font_number_6.png').convert_alpha()
num_surf_6 = transform_png(num_surf_6)
num_rect_6 = num_surf_6.get_rect(midbottom = (480, 200))

num_surf_7 = pygame.image.load(assets_dir / 'roboto_font_number_7.png').convert_alpha()
num_surf_7 = transform_png(num_surf_7)
num_rect_7 = num_surf_7.get_rect(midbottom = (580, 200))

num_surf_8 = pygame.image.load(assets_dir / 'roboto_font_number_8.png').convert_alpha()
num_surf_8 = transform_png(num_surf_8)
num_rect_8 = num_surf_8.get_rect(midbottom = (680, 200))

num_surf_9 = pygame.image.load(assets_dir / 'roboto_font_number_9.png').convert_alpha()
num_surf_9 = transform_png(num_surf_9)
num_rect_9 = num_surf_9.get_rect(midbottom = (780, 200))


# Draw the board with empty cells
def draw_grid():
    for row in range(grid_size):
        i = 0
        for col in range(grid_size):
            rect = pygame.Rect(offset + col * cell_size, offset + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(window, 'gray', rect, 1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    highlight_cell(rect)


# Function to highlight the clicked cell
def highlight_cell(rect):
    pygame.draw.rect(window, 'yellow', rect, 5)

# # Highlight a cell
# def highlight_cell(rect):
#     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#         mouse_pos = pygame.mouse.get_pos()
#         if rect.collidepoint(mouse_pos):
#             highlight_cell(rect)

# Button to auto-solve the game
solve_button_surf = pygame.image.load(assets_dir / 'solve_with_strategy.png').convert_alpha()
solve_button_surf = surf = pygame.transform.scale(solve_button_surf, (250, 40))
solve_button_rect = solve_button_surf.get_rect(center = (400, 760))
        
while True:
    # Check for all inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw the board
    draw_grid()

    # draw dark borders
    for i in range(75, 725, 216):
        window.blit(border_vertical_dark, (i, 75))
        window.blit(border_horizontal_dark, (75, i))


    # Draw the "Auto solve" button
    window.blit(solve_button_surf, solve_button_rect)


    # Draw the initial board
    # draw_initial_board

    # Register if the button was clicked


    window.blit(num_surf_1, num_rect_1)
    window.blit(num_surf_2, num_rect_2)
    window.blit(num_surf_3, num_rect_3)
    window.blit(num_surf_4, num_rect_4)
    window.blit(num_surf_5, num_rect_5)
    window.blit(num_surf_6, num_rect_6)
    window.blit(num_surf_7, num_rect_7)
    window.blit(num_surf_8, num_rect_8)
    window.blit(num_surf_9, num_rect_9)

    # update everything
    pygame.display.update()
    clock.tick(60)  # The while loop should not run more than 60 times per second