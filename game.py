import pygame
import random
import sys

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
player_image = pygame.transform.scale(pygame.image.load("assets/images/plate.png"), (player_width, player_height))  # Scale the images
player_speed = 15

# Food
food_width = 80  # Increase the size of food
food_height = 80  # Increase the size of food
food_speed = 4
food_limit = 8
food_generate_delay = 60  # Delay between generating each food item
good_food_images = [
    pygame.transform.scale(pygame.image.load("assets/images/07_bread.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/15_burger.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/22_cheesecake.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/38_friedegg.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/42_eggtart.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/22_cheesecake.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/38_friedegg.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/42_eggtart.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/54_hotdog.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/73_omlet.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/81_pizza.png"), (food_width, food_height)),  # Scale the images
    pygame.transform.scale(pygame.image.load("assets/images/92_sandwich.png"), (food_width, food_height)),  # Scale the images
]
bad_food_image = pygame.transform.scale(pygame.image.load("assets/images/dubious_food.png"), (food_width, food_height))  # Scale the image
good_food_sound = pygame.mixer.Sound("assets/sounds/yum_roblox_turkey_leg.mp3")
bad_food_sound = pygame.mixer.Sound("assets/sounds/vine_boom.mp3")

# Game Variables
score = 0
start_time = pygame.time.get_ticks()
food_list = []
food_positions = [] 

def draw_player(player_x, player_y):
    screen.blit(player_image, (player_x, player_y))

def draw_food(x, y, food):
    screen.blit(food['image'], (x, y))

def draw_score(score):
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

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
    title_text = menu_font.render("Sherman Dining: The Game", True, BLACK)
    start_text = font.render("Start Game", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Load background image
    background = pygame.image.load("assets/images/brandeis_dining.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Draw background
    screen.blit(background, (0, 0))

    # Draw the overlay on top of the background
    screen.blit(draw_overlay(), (0, 0))

    # Render and draw the text on top of the overlay
    title_text = menu_font.render("Sherman Dining: The Game", True, BLACK)
    start_text = font.render("Start Game", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))

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

def draw_game_over(background, player_x, player_y, food_list):
    game_over_text = menu_font.render("You got food poisoning!", True, BLACK)
    try_again_text = font.render("Try Again", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
    screen.blit(try_again_text, (WIDTH // 2 - try_again_text.get_width() // 2, 200))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))

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


def game_over(background, player_x, player_y, food_list):
    global score, level, start_time

    while True:
        if draw_game_over(background, player_x, player_y, food_list):
            reset_game_state()
            return True
        else:
            return False

def next_level():
    global food_speed, food_limit, level
    food_limit += 1
    food_speed += 0.5

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
    global score, start_time, level, food_speed, food_list, food_limit

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
        background = pygame.image.load("assets/images/sherman.jpg")
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
                        score -= 7
                        bad_food_sound.play()

                    if score < 0:
                        if game_over(background, player_x, player_y, food_list):
                            break

                    if score >= 10:
                        next_level()
                    
                    food_list.remove(food)

                # Remove food if it goes out of screen
                if food['y'] > HEIGHT:
                    food_list.remove(food)

            # Draw score, level, and timer
            draw_score(score)

            # Draw timer
            if not paused:  # Update timer only when the game is not paused
                current_time = pygame.time.get_ticks()  # Get current time
                elapsed_time = (current_time - start_time) // 1000  # Calculate elapsed time in seconds
                draw_timer(elapsed_time)


            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()
