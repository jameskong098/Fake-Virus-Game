import pygame
import random
import sys

version = "1.2.0"

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sherman Dining: The Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 30)
menu_font = pygame.font.SysFont(None, 40)

# Player
player_width = 90
player_height = 90
player_image = pygame.transform.scale(pygame.image.load("assets/images/plate.png"), (player_width, player_height)) 
player_speed = 15

# Food
food_width = 80  # Increase the size of food
food_height = 80  # Increase the size of food
food_speed = 4
food_limit = 8
food_generate_delay = 60  # Delay between generating each food item
good_food_images = [
    pygame.transform.scale(pygame.image.load("assets/images/07_bread.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/15_burger.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/38_friedegg.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/22_cheesecake.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/54_hotdog.png"), (food_width, food_height)), 
    pygame.transform.scale(pygame.image.load("assets/images/73_omlet.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/81_pizza.png"), (food_width, food_height)),  
    pygame.transform.scale(pygame.image.load("assets/images/92_sandwich.png"), (food_width, food_height)), 
    pygame.transform.scale(pygame.image.load("assets/images/79_pancakes.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/85_roastedchicken.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/88_salmon.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/28_cookies.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/57_icecream.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/67_macncheese.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/44_frenchfries.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/69_meatball.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/94_spaghetti.png"), (food_width, food_height)),
    pygame.transform.scale(pygame.image.load("assets/images/97_sushi.png"), (food_width, food_height))
]
bad_food_image = pygame.transform.scale(pygame.image.load("assets/images/dubious_food.png"), (food_width, food_height)) 
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
pygame.mixer.music.set_volume(0.1)  # Adjust volume if needed

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

def draw_high_score():
    text = font.render("High Score: " + str(high_score), True, BLACK)
    screen.blit(text, (WIDTH - text.get_width() - 10, 10))

# Update high score
def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

def draw_player(player_x, player_y):
    screen.blit(player_image, (player_x, player_y))

def draw_food(x, y, food):
    screen.blit(food['image'], (x, y))

def draw_score(score):
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

def draw_lives(lives):
    text = font.render("Lives: " + str(lives), True, BLACK)
    screen.blit(text, (10, 40))

def draw_timer(time_passed):
    text = font.render("Time: " + str(time_passed), True, BLACK)
    screen.blit(text, (WIDTH // 2 - 50, 10))

def draw_overlay():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)  # Adjust the transparency level as needed
    overlay.fill(WHITE)  # Fill the overlay with a white color
    return overlay

def draw_menu():
    global version, menu_bg_image
    title_text = menu_font.render("Sherman Dining: The Game", True, BLACK)
    start_text = font.render("Start Game", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Versioning text
    version_text = font.render(version, True, BLACK)
    version_text_x = WIDTH // 2 - version_text.get_width() // 2
    version_text_y = HEIGHT - 50  # Adjust this value to change the vertical position

    # Load background image
    background = menu_bg_image
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Draw background
    screen.blit(background, (0, 0))

    # Draw the overlay on top of the background
    screen.blit(draw_overlay(), (0, 0))

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))
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
                if 200 <= y <= 250:
                    return True
                elif 250 <= y <= 300:
                    pygame.quit()
                    sys.exit()

def draw_game_over(score, time_passed):
    game_over_text = menu_font.render("You got food poisoning!", True, BLACK)
    try_again_text = font.render("Try Again", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)
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
    try_again_y = time_y + vertical_spacing
    quit_y = try_again_y + vertical_spacing

    screen.blit(game_over_text, (game_over_x, game_over_y))
    screen.blit(score_text, (score_x, score_y))
    screen.blit(high_score_text, (high_score_x, high_score_y))
    screen.blit(time_text, (time_x, time_y))
    screen.blit(try_again_text, (try_again_x, try_again_y))
    screen.blit(quit_text, (quit_x, quit_y))


    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 200 <= y <= 250:
                    return True
                elif 250 <= y <= 300:
                    pygame.quit()
                    sys.exit()

def draw_pause_menu(background, player_x, player_y, food_list):
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

    # Draw the pause menu on top
    pause_text = menu_font.render("Paused", True, BLACK)
    resume_text = font.render("Resume", True, BLACK)
    quit_text = font.render("Quit to Menu", True, BLACK)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 100))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 200 <= y <= 250:  # Resume
                    return True
                elif 250 <= y <= 300:  # Quit to menu
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
    global score, start_time, player_x, player_y, food_list
    score = 0
    start_time = pygame.time.get_ticks()
    # Reset player position
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 120
    # Reset food list
    food_list = []


def main():
    global score, start_time, level, food_speed, food_list, food_limit, lives, game_bg_image

    while True:
        if not draw_menu():
            break

        reset_game_state()  # Reset game state

        player_x = WIDTH // 2 - player_width // 2
        player_y = HEIGHT - 120 
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        player_velocity = [0, 0]  # Store player velocity when paused

        clock = pygame.time.Clock()
        running = True
        paused = False

        # Load background image
        background = game_bg_image
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

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
                    if event.key == pygame.K_p:
                        if paused:
                            # Unpause the game
                            paused = False
                            # Restore player velocity
                            player_velocity = [0, 0]
                        else:
                            # Pause the game
                            paused = True

            if paused:
                paused = not draw_pause_menu(background, player_x, player_y, food_list)  # Check if game should resume
                continue
            
            if not paused:
                # Move player
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player_x > 0:
                    player_x -= player_speed
                if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
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

                # Check collision with player
                food_rect = pygame.Rect(food['x'], food['y'], food_width, food_height)
                if food_rect.colliderect(player_rect):
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
