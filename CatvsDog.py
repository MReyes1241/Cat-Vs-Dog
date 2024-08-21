import pygame
import os

# Initialize pygame modules
pygame.font.init()
pygame.mixer.init()

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to assets (relative to the script's location)
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

DOG_FIRE_SOUND_PATH = os.path.join(ASSETS_DIR, "Dog.wav")
CAT_FIRE_SOUND_PATH = os.path.join(ASSETS_DIR, "Meow.wav")
HIT_SFX_PATH = os.path.join(ASSETS_DIR, "Hit.wav")
DOG_IMAGE_PATH = os.path.join(ASSETS_DIR, "cute_dog_image.gif")
CAT_IMAGE_PATH = os.path.join(ASSETS_DIR, "cute_cat_image.png")
SPACE_IMAGE_PATH = os.path.join(ASSETS_DIR, "space.jpeg")

# Window dimensions and settings
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cat Vs Dog')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Border settings
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Load sounds
DOG_FIRE_SOUND = pygame.mixer.Sound(DOG_FIRE_SOUND_PATH)
CAT_FIRE_SOUND = pygame.mixer.Sound(CAT_FIRE_SOUND_PATH)
HIT_SFX = pygame.mixer.Sound(HIT_SFX_PATH)

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
END_FONT = pygame.font.SysFont('comicsans', 70)

# Game settings
FPS = 60
ANIMAL_WIDTH, ANIMAL_HEIGHT = 60, 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4

# User events
PLAY1_HIT = pygame.USEREVENT + 1
PLAY2_HIT = pygame.USEREVENT + 2

# Load images
GOLDEN_DOG_IMAGE = pygame.image.load(DOG_IMAGE_PATH)
GOLDEN_DOG = pygame.transform.scale(GOLDEN_DOG_IMAGE, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
MINY_CAT_IMAGE = pygame.image.load(CAT_IMAGE_PATH)
MINY_CAT = pygame.transform.scale(MINY_CAT_IMAGE, (ANIMAL_WIDTH, ANIMAL_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load(SPACE_IMAGE_PATH), (WIDTH, HEIGHT))

def draw_window(play1, play2, play1_bullets, play2_bullets, play1_health, play2_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    play1_health_text = HEALTH_FONT.render("Health: " + str(play1_health), 1, WHITE)
    play2_health_text = HEALTH_FONT.render("Health: " + str(play2_health), 1, WHITE)
    WIN.blit(play1_health_text, (WIDTH - play1_health_text.get_width() - 10, 10))
    WIN.blit(play2_health_text, (10, 10))

    WIN.blit(GOLDEN_DOG, (play1.x, play1.y))
    WIN.blit(MINY_CAT, (play2.x, play2.y))

    for bullet in play1_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in play2_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()

def play1_handle_movement(keys_pressed, play1):
    if keys_pressed[pygame.K_a] and play1.x - VEL > 0:  # left
        play1.x -= VEL
    if keys_pressed[pygame.K_d] and play1.x + VEL + play1.width < BORDER.x:  # right
        play1.x += VEL
    if keys_pressed[pygame.K_s] and play1.y + VEL + play1.height < HEIGHT:  # down
        play1.y += VEL
    if keys_pressed[pygame.K_w] and play1.y - VEL > 0:  # up
        play1.y -= VEL

def play2_handle_movement(keys_pressed, play2):
    if keys_pressed[pygame.K_LEFT] and play2.x - VEL > BORDER.x + BORDER.width:  # left
        play2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and play2.x + VEL + play2.width < WIDTH:  # right
        play2.x += VEL
    if keys_pressed[pygame.K_DOWN] and play2.y + VEL + play2.height < HEIGHT:  # down
        play2.y += VEL
    if keys_pressed[pygame.K_UP] and play2.y - VEL > 0:  # up
        play2.y -= VEL

def handle_bullets(play1_bullets, play2_bullets, play1, play2):
    for bullet in play1_bullets:
        bullet.x += BULLET_VEL
        if play2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAY2_HIT))
            play1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            play1_bullets.remove(bullet)

    for bullet in play2_bullets:
        bullet.x -= BULLET_VEL
        if play1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAY1_HIT))
            play2_bullets.remove(bullet)
        elif bullet.x < 0:
            play2_bullets.remove(bullet)

def draw_end(text):
    draw_text = END_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    play1 = pygame.Rect(100, 300, ANIMAL_WIDTH, ANIMAL_HEIGHT)
    play2 = pygame.Rect(700, 300, ANIMAL_WIDTH, ANIMAL_HEIGHT)

    play1_bullets = []
    play2_bullets = []

    play1_health = 3
    play2_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(play1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(play1.x + play1.width, play1.y + play1.height // 2 - 5, 10, 5)
                    play1_bullets.append(bullet)
                    DOG_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(play2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(play2.x, play2.y + play2.height // 2 - 5, 10, 5)
                    play2_bullets.append(bullet)
                    CAT_FIRE_SOUND.play()

            if event.type == PLAY1_HIT:
                play1_health -= 1
                HIT_SFX.play()

            if event.type == PLAY2_HIT:
                play2_health -= 1
                HIT_SFX.play()

        end_game_text = ""
        if play1_health <= 0:
            end_game_text = "Player 2 Wins!"
        if play2_health <= 0:
            end_game_text = "Player 1 Wins!"
        if end_game_text != "":
            draw_end(end_game_text)
            break

        keys_pressed = pygame.key.get_pressed()
        play1_handle_movement(keys_pressed, play1)
        play2_handle_movement(keys_pressed, play2)

        handle_bullets(play1_bullets, play2_bullets, play1, play2)

        draw_window(play1, play2, play1_bullets, play2_bullets, play1_health, play2_health)

    pygame.quit()

if __name__ == "__main__":
    main()
