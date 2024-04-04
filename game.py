import pygame
import random
import sys

version = "1.2.3"

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sherman Dining: The Game")
icon_image = pygame.image.load("assets/images/brandeis_logo.jpg")
pygame.display.set_icon(icon_image)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 30)
menu_font = pygame.font.SysFont(None, 40)
text_color = BLACK
text_bg = WHITE

# Player
player_width = 90
player_height = 90
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120
player_image = pygame.transform.scale(pygame.image.load("assets/images/plate.png"), (player_width, player_height)) 
player_speed = 15

# Food
food_width = 80  
food_height = 80  
food_speed = 4
food_limit = 8
food_generate_delay = 60  # Delay between generating each food item
good_food_images = [
    pygame.transform.scale(pygame.image.load("assets/images/food/07_bread.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/15_burger.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/38_friedegg.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/22_cheesecake.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/54_hotdog.png"), (food_width, food_height)), 
    pygame.transform.scale(pygame.image.load("assets/images/food/73_omlet.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/81_pizza.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/food/92_sandwich.png"), (food_width, food_height)), 
    pygame.transform.scale(pygame.image.load("assets/images/food/79_pancakes.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/85_roastedchicken.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/88_salmon.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/28_cookies.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/57_icecream.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/67_macncheese.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/44_frenchfries.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/69_meatball.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/94_spaghetti.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/food/97_sushi.png"), (food_width, food_height))
]
bad_food_image = pygame.transform.scale(pygame.image.load("assets/images/food/dubious_food.png"), (food_width, food_height)) 
good_food_sound = pygame.mixer.Sound("assets/sounds/yum_roblox_turkey_leg.mp3")
good_food_sound.set_volume(0.5)
bad_food_sound = pygame.mixer.Sound("assets/sounds/vine_boom.mp3")
bad_food_sound.set_volume(0.3)

# Menu Background
menu_bg_image = pygame.image.load("assets/images/brandeis_dining.jpg")

# Game Background
game_bg_image = pygame.image.load("assets/images/sherman.jpg")

# Background Music
background_music = "assets/sounds/spiderman_game_pizza_theme.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.1) 

# Game Variables
score = 0
lives = 3
start_time = pygame.time.get_ticks()
food_list = []
food_positions = [] 

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Load high score
high_score = load_high_score()

# Update high score
def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

def draw_high_score():
    text_surface = font.render("High Score: " + str(high_score), True, text_color)
    background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
    background_surface.fill(text_bg)
    screen.blit(background_surface, (WIDTH - text_surface.get_width() - 10, 10))
    screen.blit(text_surface, (WIDTH - text_surface.get_width() - 10, 10))

def draw_player(player_x, player_y):
    screen.blit(player_image, (player_x, player_y))

def draw_food(x, y, food):
    screen.blit(food['image'], (x, y))

def draw_score(score):
    text_surface = font.render("Score: " + str(score), True, text_color)
    background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
    background_surface.fill(text_bg)
    screen.blit(background_surface, (10, 10))
    screen.blit(text_surface, (10, 10))

def draw_lives(lives):
    text_surface = font.render("Lives: " + str(lives), True, text_color)
    background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
    background_surface.fill(text_bg)
    screen.blit(background_surface, (10, 40))
    screen.blit(text_surface, (10, 40))

def draw_timer(time_passed):
    text_surface = font.render("Time: " + str(time_passed), True, text_color)
    background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
    background_surface.fill(text_bg)
    screen.blit(background_surface, (WIDTH // 2 - 50, 10))
    screen.blit(text_surface, (WIDTH // 2 - 50, 10))

def draw_overlay():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)  
    overlay.fill(WHITE) 
    return overlay

def draw_menu():
    global version, menu_bg_image, text_color, text_bg
    title_text = menu_font.render("Sherman Dining: The Game", True, text_color)
    start_text = font.render("Start Game", True, text_color)
    quit_text = font.render("Quit", True, text_color)

    # Versioning text
    version_text = font.render(version, True, BLACK)
    version_text_x = WIDTH // 2 - version_text.get_width() // 2
    version_text_y = HEIGHT - 50 

    # Load background image
    background = menu_bg_image
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Draw background
    screen.blit(background, (0, 0))

    # Draw the overlay on top of the background
    screen.blit(draw_overlay(), (0, 0))

    # Draw title text with background
    title_bg_rect = pygame.Rect(WIDTH // 2 - title_text.get_width() // 2 - 10, 90, title_text.get_width() + 20, title_text.get_height() + 10)
    pygame.draw.rect(screen, text_bg, title_bg_rect)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Draw start game text with background
    start_bg_rect = pygame.Rect(WIDTH // 2 - start_text.get_width() // 2 - 10, 290, start_text.get_width() + 20, start_text.get_height() + 10)
    pygame.draw.rect(screen, text_bg, start_bg_rect)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 300))

    # Draw quit text with background
    quit_bg_rect = pygame.Rect(WIDTH // 2 - quit_text.get_width() // 2 - 10, 390, quit_text.get_width() + 20, quit_text.get_height() + 10)
    pygame.draw.rect(screen, text_bg, quit_bg_rect)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 400))

    screen.blit(version_text, (version_text_x, version_text_y))

    pygame.display.update()

    # Start playing background music
    pygame.mixer.music.play(loops=-1)  # Set loops to -1 to loop indefinitely

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= y <= 350: # Start Game Button
                    return True
                elif 400 <= y <= 450: # Quit Game Button
                    pygame.quit()
                    sys.exit()

def draw_game_over(score, time_passed):
    game_over_text = menu_font.render("You got food poisoning!", True, BLACK)
    try_again_text = font.render("Try Again", True, BLACK)
    quit_text = font.render("Quit to Menu", True, BLACK)
    score_text = font.render("Score: " + str(score), True, BLACK)
    high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
    time_text = font.render("Time: " + str(time_passed), True, BLACK)

     # Calculate positions for the text
    game_over_x = WIDTH // 2 - game_over_text.get_width() // 2
    try_again_x = WIDTH // 2 - try_again_text.get_width() // 2
    quit_x = WIDTH // 2 - quit_text.get_width() // 2
    score_x = WIDTH // 2 - score_text.get_width() // 2
    high_score_x = WIDTH // 2 - high_score_text.get_width() // 2
    time_x = WIDTH // 2 - time_text.get_width() // 2

    # Set vertical positions
    vertical_spacing = 50
    game_over_y = 100
    score_y = game_over_y + vertical_spacing
    high_score_y = score_y + vertical_spacing
    time_y = high_score_y + vertical_spacing
    try_again_y = time_y + 2 * vertical_spacing  
    quit_y = try_again_y + 2 * vertical_spacing 

    game_over_bg = pygame.Surface((game_over_text.get_width(), game_over_text.get_height()))
    game_over_bg.fill(text_bg)
    screen.blit(game_over_bg, (game_over_x, game_over_y))
    screen.blit(game_over_text, (game_over_x, game_over_y))

    score_bg = pygame.Surface((score_text.get_width(), score_text.get_height()))
    score_bg.fill(text_bg)
    screen.blit(score_bg, (score_x, score_y))
    screen.blit(score_text, (score_x, score_y))

    high_score_bg = pygame.Surface((high_score_text.get_width(), high_score_text.get_height()))
    high_score_bg.fill(text_bg)
    screen.blit(high_score_bg, (high_score_x, high_score_y))
    screen.blit(high_score_text, (high_score_x, high_score_y))

    time_bg = pygame.Surface((time_text.get_width(), time_text.get_height()))
    time_bg.fill(text_bg)
    screen.blit(time_bg, (time_x, time_y))
    screen.blit(time_text, (time_x, time_y))

    try_again_bg = pygame.Surface((try_again_text.get_width(), try_again_text.get_height()))
    try_again_bg.fill(text_bg)
    screen.blit(try_again_bg, (try_again_x, try_again_y))
    screen.blit(try_again_text, (try_again_x, try_again_y))

    quit_bg = pygame.Surface((quit_text.get_width(), quit_text.get_height()))
    quit_bg.fill(text_bg)
    screen.blit(quit_bg, (quit_x, quit_y))
    screen.blit(quit_text, (quit_x, quit_y))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if try_again_y <= y <= try_again_y + try_again_text.get_height():  
                    return True
                elif quit_y <= y <= quit_y + quit_text.get_height():  
                    return False

def draw_pause_menu(background, food_list):
    global lives, player_x, player_y

    # Redraw background so that pause menu os on top
    screen.blit(background, (0, 0))

    # Draw the overlay on top of the background
    screen.blit(draw_overlay(), (0, 0))

    # Draw player
    draw_player(player_x, player_y)

    # Draw and move food
    for food in food_list:
        draw_food(food['x'], food['y'], food)

    # Draw score, level, and timer
    draw_score(score)
    time_passed = (pygame.time.get_ticks() - start_time) // 1000
    draw_timer(time_passed)
    draw_high_score()
    draw_lives(lives)

    # Draw the pause menu on top
    pause_text = menu_font.render("Paused", True, text_color)
    resume_text = font.render("Resume", True, text_color)
    quit_text = font.render("Quit to Menu", True, text_color)

    # Draw background for the text
    pause_bg_rect = pygame.Rect(WIDTH // 2 - pause_text.get_width() // 2 - 10, 100, pause_text.get_width() + 20, pause_text.get_height() + 10)
    resume_bg_rect = pygame.Rect(WIDTH // 2 - resume_text.get_width() // 2 - 10, 200, resume_text.get_width() + 20, resume_text.get_height() + 10)
    quit_bg_rect = pygame.Rect(WIDTH // 2 - quit_text.get_width() // 2 - 10, 300, quit_text.get_width() + 20, quit_text.get_height() + 10)

    pygame.draw.rect(screen, text_bg, pause_bg_rect)
    pygame.draw.rect(screen, text_bg, resume_bg_rect)
    pygame.draw.rect(screen, text_bg, quit_bg_rect)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 100))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 300))  

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 200 <= y <= 250:  # Resume
                    return True
                elif 300 <= y <= 350:  # Quit to menu
                    return False



def generate_food():
    global food_positions
    # Generate food at random x-coordinates, ensuring they don't overlap
    while True:
        x = random.randint(0, WIDTH - food_width)
        if x not in food_positions:  # Check if position is already occupied
            food_positions.append(x)
            break
    y = -food_height  # Start from the top of the screen
    is_good = random.choice([True, False])
    if is_good:
        food_image = random.choice(good_food_images)
        return {'x': x, 'y': y, 'image': food_image, 'is_good': True}
    else:
        return {'x': x, 'y': y, 'image': bad_food_image, 'is_good': False}


def game_over(score, elapsed_time):
    global level, start_time

    while True:
        if draw_game_over(score, elapsed_time):
            reset_game_state()
            return True
        else:
            return False

def next_level():
    global food_speed, food_limit, level
    food_speed += 0.1

def reset_game_state():
    global score, start_time, player_x, player_y, food_list, lives
    score = 0
    start_time = pygame.time.get_ticks()
    player_x = WIDTH // 2 - player_width // 2  
    player_y = HEIGHT - 120  
    food_list = []
    lives = 3

def main():
    global score, start_time, player_x, player_y, level, food_speed, food_list, food_limit, lives, game_bg_image

    while True:
        if not draw_menu():
            break

        reset_game_state()

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        clock = pygame.time.Clock()
        running = True
        paused = False

        # Load background image
        background = game_bg_image
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        # Reset start time when the game starts
        start_time = pygame.time.get_ticks()

        while running:
            # Draw background
            screen.blit(background, (0, 0))

            # Draw the overlay on top of the background
            screen.blit(draw_overlay(), (0, 0))

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:  # Pause/Unpause on "P" or "Esc" key
                        if paused:
                            # Unpause the game
                            paused = False
                            # Restore player velocity
                            player_velocity = [0, 0]
                        else:
                            # Pause the game
                            paused = True

            if paused:
                if not draw_pause_menu(background, food_list):  # Check if game should resume
                    running = False  
                else:
                    paused = False  # Resume the game if draw_pause_menu returns True
            
            
            if not paused:
                # Move player
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
                    player_x -= player_speed
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
                    player_x += player_speed
                
                # Update player's rectangle
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            # Generate food
            if len(food_list) < food_limit and pygame.time.get_ticks() % food_generate_delay == 0:  # Limit the number of foods on screen
                food_list.append(generate_food())

            # Draw player
            draw_player(player_x, player_y)

            # Draw and move food
            for food in food_list:
                draw_food(food['x'], food['y'], food)
                food['y'] += food_speed

                # Load the masks for player and food images
                player_mask = pygame.mask.from_surface(player_image)
                food_mask = pygame.mask.from_surface(food['image'])

                # Check collision using masks
                if player_mask.overlap(food_mask, (food['x'] - player_x, food['y'] - player_y)):
                    if food['is_good']:
                        score += 5
                        good_food_sound.play()
                    else:
                        lives -= 1
                        bad_food_sound.play()

                    if lives == 0:
                        current_time = pygame.time.get_ticks()  # Get current time
                        elapsed_time = (current_time - start_time) // 1000  # Calculate elapsed time in seconds
                        if game_over(score, elapsed_time):
                            break
                        else:
                            running = False

                    if score % 10 == 0:
                        next_level()
                    
                    food_list.remove(food)

                # Remove food if it goes out of screen
                if food['y'] > HEIGHT:
                    food_list.remove(food)

            update_high_score(score)

            # Draw score, lives, high score, and timer
            draw_score(score)
            draw_lives(lives)
            draw_high_score()

            # Draw timer
            if not paused:  # Update timer only when the game is not paused
                current_time = pygame.time.get_ticks()  # Get current time
                elapsed_time = (current_time - start_time) // 1000  # Calculate elapsed time in seconds
                draw_timer(elapsed_time)

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()
