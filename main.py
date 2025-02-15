import pygame, sys, os
from game import Game
from colors import Colors

pygame.init()

# Set base path based on whether the script is running from source or bundled executable
if getattr(sys, 'frozen', False):
    # If running as a bundled app, e.g., from main.exe
    base_path = sys._MEIPASS
else:
    # If running in a normal Python environment
    base_path = os.path.dirname(__file__)

# Example: Load the icon from the cover folder
icon_path = os.path.join(base_path, 'cover', 'tetris_icon.ico')
try:
    window_icon = pygame.image.load(icon_path)
    pygame.display.set_icon(window_icon)
except pygame.error:
    print(f"Error: Could not load {icon_path}. Make sure the file exists.")

lavender = (153, 153, 255)
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
reset_rect = pygame.Rect(320, 420, 170, 60)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game = Game()

def draw_buttons():
    easy_button = pygame.Rect(150, 220, 200, 60)
    medium_button = pygame.Rect(150, 300, 200, 60)
    hard_button = pygame.Rect(150, 380, 200, 60)
    
    pygame.draw.rect(screen, Colors.light_blue, easy_button, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, medium_button, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, hard_button, 0, 10)
    
    easy_text = title_font.render("Easy", True, Colors.white)
    medium_text = title_font.render("Medium", True, Colors.white)
    hard_text = title_font.render("Hard", True, Colors.white)
    
    screen.blit(easy_text, (easy_button.x + 70, easy_button.y + 20))
    screen.blit(medium_text, (medium_button.x + 50, medium_button.y + 20))
    screen.blit(hard_text, (hard_button.x + 70, hard_button.y + 20))

    return easy_button, medium_button, hard_button

def draw_reset_button():
    pygame.draw.rect(screen, Colors.light_blue, reset_rect, 0, 10)
    reset_text = title_font.render("Reset", True, Colors.white)
    screen.blit(reset_text, (reset_rect.x + 50, reset_rect.y + 20))

def draw_title():
    # Load the title image from the cover folder
    title_image_path = os.path.join(base_path, 'cover', 'tetris_title.png')
    try:
        title_image = pygame.image.load(title_image_path)
        title_image = pygame.transform.scale(title_image, (250, 80))
        screen.blit(title_image, (125, 50))
    except pygame.error:
        print(f"Error: Could not load {title_image_path}. Make sure the file exists.")

def show_speed_select_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                easy_button, medium_button, hard_button = draw_buttons()
                if easy_button.collidepoint(pos):
                    pygame.time.set_timer(GAME_UPDATE, 500)
                    game.game_over = False
                    game.reset()
                    running = False
                elif medium_button.collidepoint(pos):
                    pygame.time.set_timer(GAME_UPDATE, 300)
                    game.game_over = False
                    game.reset()
                    running = False
                elif hard_button.collidepoint(pos):
                    pygame.time.set_timer(GAME_UPDATE, 200)
                    game.game_over = False
                    game.reset()
                    running = False
        screen.fill(lavender)
        draw_title()
        draw_buttons()
        pygame.display.update()
        clock.tick(60)

GAME_UPDATE = pygame.USEREVENT
show_speed_select_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()
            if event.key == pygame.K_DOWN and not game.game_over:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if reset_rect.collidepoint(pos):
                game.game_over = True
                game.reset()
                show_speed_select_screen()

    screen.fill(lavender)
    screen.blit(score_surface, (365, 20))
    screen.blit(next_surface, (375, 180))
    if game.game_over:
        screen.blit(game_over_surface, (320, 450))
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)
    draw_reset_button()
    pygame.display.update()
    clock.tick(60)
