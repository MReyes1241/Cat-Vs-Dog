import pygame
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (20, 30, 60)
LIGHT_BLUE = (100, 150, 255)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)

FPS = 60
ANIMAL_WIDTH, ANIMAL_HEIGHT = 60, 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Create window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cat Vs Dog')

# Create border - now invisible, just for collision detection
BORDER = pygame.Rect(WIDTH // 2 - 2, 0, 4, HEIGHT)

# Global sound setting
SOUND_ENABLED = True

# Load assets with fallbacks
def load_image(path, size, fallback_color, text):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        font = pygame.font.Font(None, 20)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text_surf, text_rect)
        return surface

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return pygame.mixer.Sound(pygame.array.array('h', [0] * 100))

def play_sound(sound):
    if SOUND_ENABLED:
        sound.play()

# Load assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

DOG_IMAGE = load_image(os.path.join(ASSETS_DIR, "cute_dog_image.gif"), 
                       (ANIMAL_WIDTH, ANIMAL_HEIGHT), RED, "DOG")
CAT_IMAGE = load_image(os.path.join(ASSETS_DIR, "cute_cat_image.png"), 
                       (ANIMAL_WIDTH, ANIMAL_HEIGHT), BLUE, "CAT")

# Create space background
try:
    SPACE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "space.jpeg")), (WIDTH, HEIGHT))
except:
    # Create sleek gradient background with animated stars
    SPACE = pygame.Surface((WIDTH, HEIGHT))
    # Create a blue-to-black gradient
    for y in range(HEIGHT):
        progress = y / HEIGHT
        r = int(10 * (1 - progress))
        g = int(20 * (1 - progress))
        b = int(60 * (1 - progress))
        pygame.draw.line(SPACE, (r, g, b), (0, y), (WIDTH, y))
    
    # Add scattered stars of different sizes
    for i in range(150):
        x = int(pygame.random.random() * WIDTH)
        y = int(pygame.random.random() * HEIGHT)
        size = pygame.random.choice([1, 1, 1, 2, 2, 3])  # Mostly small stars
        brightness = pygame.random.randint(150, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(SPACE, color, (x, y), size)

DOG_FIRE_SOUND = load_sound(os.path.join(ASSETS_DIR, "Dog.wav"))
CAT_FIRE_SOUND = load_sound(os.path.join(ASSETS_DIR, "Meow.wav"))
HIT_SOUND = load_sound(os.path.join(ASSETS_DIR, "Hit.wav"))

# Fonts
TITLE_FONT = pygame.font.Font(None, 80)
MENU_FONT = pygame.font.Font(None, 50)
HEALTH_FONT = pygame.font.Font(None, 40)
SMALL_FONT = pygame.font.Font(None, 30)

# Events
DOG_HIT = pygame.USEREVENT + 1
CAT_HIT = pygame.USEREVENT + 2

def draw_sleek_ui_panel(surface, x, y, width, height, color, alpha=180):
    """Draw a sleek UI panel with rounded corners and transparency"""
    panel = pygame.Surface((width, height))
    panel.set_alpha(alpha)
    panel.fill(color)
    surface.blit(panel, (x, y))
    
    # Add a subtle border
    border_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2)

def draw_center_line():
    """Draw a subtle center line instead of the harsh black bar"""
    # Draw a subtle gradient line down the center
    center_x = WIDTH // 2
    
    # Create a thin vertical gradient
    for y in range(HEIGHT):
        alpha = int(30 * (1 - abs(y - HEIGHT//2) / (HEIGHT//2)))  # Fade from center
        color = (*LIGHT_BLUE, alpha)
        
        # Draw a thin line with fading effect
        line_surface = pygame.Surface((4, 1))
        line_surface.set_alpha(alpha)
        line_surface.fill(LIGHT_BLUE)
        WIN.blit(line_surface, (center_x - 2, y))
def draw_menu():
    WIN.blit(SPACE, (0, 0))
    
    # Sleek title with glow effect
    title = TITLE_FONT.render("Cat Vs Dog", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    # Add glow effect by drawing the title multiple times with decreasing alpha
    glow_surface = pygame.Surface((title.get_width() + 20, title.get_height() + 20))
    glow_surface.set_alpha(50)
    glow_title = TITLE_FONT.render("Cat Vs Dog", True, LIGHT_BLUE)
    glow_surface.blit(glow_title, (10, 10))
    WIN.blit(glow_surface, (title_rect.x - 10, title_rect.y - 10))
    
    WIN.blit(title, title_rect)
    
    # Sleek menu panel
    panel_width = 400
    panel_height = 200
    panel_x = WIDTH//2 - panel_width//2
    panel_y = HEIGHT//2 - 30
    
    draw_sleek_ui_panel(WIN, panel_x, panel_y, panel_width, panel_height, DARK_BLUE, 120)
    
    # Menu options with better styling
    start_text = MENU_FONT.render("Press SPACE to Start", True, NEON_GREEN)
    start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
    WIN.blit(start_text, start_rect)
    
    # Sound toggle with better colors
    sound_status = "ON" if SOUND_ENABLED else "OFF"
    sound_color = NEON_GREEN if SOUND_ENABLED else NEON_PINK
    sound_text = SMALL_FONT.render(f"Sound: {sound_status} (Press M to toggle)", True, sound_color)
    sound_rect = sound_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    WIN.blit(sound_text, sound_rect)
    
    # Controls in a separate panel
    controls_y = HEIGHT - 140
    draw_sleek_ui_panel(WIN, 50, controls_y, WIDTH - 100, 120, DARK_BLUE, 100)
    
    controls = [
        "Controls:",
        "Player 1 (Dog): WASD + Left Shift  |  Player 2 (Cat): Arrows + Right Shift",
        "Press ESC to quit anytime"
    ]
    
    y_offset = controls_y + 20
    for i, control in enumerate(controls):
        color = NEON_GREEN if i == 0 else WHITE
        font = SMALL_FONT if i == 0 else pygame.font.Font(None, 22)
        text = font.render(control, True, color)
        text_rect = text.get_rect(center=(WIDTH//2, y_offset))
        WIN.blit(text, text_rect)
        y_offset += 30
    
    pygame.display.update()

def draw_game(dog, cat, dog_bullets, cat_bullets, dog_health, cat_health):
    WIN.blit(SPACE, (0, 0))
    
    # Draw subtle center line instead of black bar
    draw_center_line()
    
    # Draw sleek health panels
    # Dog health panel (left side)
    draw_sleek_ui_panel(WIN, 10, 10, 200, 50, DARK_BLUE, 150)
    dog_health_text = HEALTH_FONT.render(f"Dog Health: {dog_health}", True, NEON_PINK)
    WIN.blit(dog_health_text, (20, 25))
    
    # Cat health panel (right side)
    cat_panel_width = 200
    draw_sleek_ui_panel(WIN, WIDTH - cat_panel_width - 10, 10, cat_panel_width, 50, DARK_BLUE, 150)
    cat_health_text = HEALTH_FONT.render(f"Cat Health: {cat_health}", True, LIGHT_BLUE)
    WIN.blit(cat_health_text, (WIDTH - cat_panel_width + 10, 25))
    
    # Draw players
    WIN.blit(DOG_IMAGE, (dog.x, dog.y))
    WIN.blit(CAT_IMAGE, (cat.x, cat.y))
    
    # Draw bullets with glow effect
    for bullet in dog_bullets:
        # Draw glow
        glow_rect = pygame.Rect(bullet.x - 2, bullet.y - 2, bullet.width + 4, bullet.height + 4)
        glow_surface = pygame.Surface((bullet.width + 4, bullet.height + 4))
        glow_surface.set_alpha(100)
        glow_surface.fill(NEON_PINK)
        WIN.blit(glow_surface, (bullet.x - 2, bullet.y - 2))
        
        # Draw bullet
        pygame.draw.rect(WIN, NEON_PINK, bullet)
    
    for bullet in cat_bullets:
        # Draw glow
        glow_surface = pygame.Surface((bullet.width + 4, bullet.height + 4))
        glow_surface.set_alpha(100)
        glow_surface.fill(LIGHT_BLUE)
        WIN.blit(glow_surface, (bullet.x - 2, bullet.y - 2))
        
        # Draw bullet
        pygame.draw.rect(WIN, LIGHT_BLUE, bullet)
    
    pygame.display.update()

def draw_game_over(winner):
    # Sleek semi-transparent overlay with gradient
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 20))  # Dark blue tint
    WIN.blit(overlay, (0, 0))
    
    # Main game over panel
    panel_width = 500
    panel_height = 300
    panel_x = WIDTH//2 - panel_width//2
    panel_y = HEIGHT//2 - panel_height//2
    
    draw_sleek_ui_panel(WIN, panel_x, panel_y, panel_width, panel_height, DARK_BLUE, 200)
    
    # Winner text with glow
    winner_color = NEON_PINK if "Dog" in winner else LIGHT_BLUE
    winner_text = TITLE_FONT.render(winner, True, winner_color)
    winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
    
    # Add glow effect
    glow_surface = pygame.Surface((winner_text.get_width() + 20, winner_text.get_height() + 20))
    glow_surface.set_alpha(80)
    glow_text = TITLE_FONT.render(winner, True, winner_color)
    glow_surface.blit(glow_text, (10, 10))
    WIN.blit(glow_surface, (winner_rect.x - 10, winner_rect.y - 10))
    
    WIN.blit(winner_text, winner_rect)
    
    # Options with better styling
    restart_text = MENU_FONT.render("Press R to Play Again", True, NEON_GREEN)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
    WIN.blit(restart_text, restart_rect)
    
    menu_text = SMALL_FONT.render("Press M for Main Menu", True, WHITE)
    menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
    WIN.blit(menu_text, menu_rect)
    
    quit_text = SMALL_FONT.render("Press ESC to Quit", True, NEON_PINK)
    quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    WIN.blit(quit_text, quit_rect)

def move_dog(keys, dog):
    if keys[pygame.K_a] and dog.x - VEL > 0:
        dog.x -= VEL
    if keys[pygame.K_d] and dog.x + VEL + dog.width < BORDER.x:
        dog.x += VEL
    if keys[pygame.K_s] and dog.y + VEL + dog.height < HEIGHT:
        dog.y += VEL
    if keys[pygame.K_w] and dog.y - VEL > 0:
        dog.y -= VEL

def move_cat(keys, cat):
    if keys[pygame.K_LEFT] and cat.x - VEL > BORDER.x + BORDER.width:
        cat.x -= VEL
    if keys[pygame.K_RIGHT] and cat.x + VEL + cat.width < WIDTH:
        cat.x += VEL
    if keys[pygame.K_DOWN] and cat.y + VEL + cat.height < HEIGHT:
        cat.y += VEL
    if keys[pygame.K_UP] and cat.y - VEL > 0:
        cat.y -= VEL

def handle_bullets(dog_bullets, cat_bullets, dog, cat):
    # Move dog bullets right
    for bullet in dog_bullets[:]:
        bullet.x += BULLET_VEL
        if cat.colliderect(bullet):
            pygame.event.post(pygame.event.Event(CAT_HIT))
            dog_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            dog_bullets.remove(bullet)
    
    # Move cat bullets left
    for bullet in cat_bullets[:]:
        bullet.x -= BULLET_VEL
        if dog.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DOG_HIT))
            cat_bullets.remove(bullet)
        elif bullet.x < 0:
            cat_bullets.remove(bullet)

def reset_game():
    dog = pygame.Rect(100, 300, ANIMAL_WIDTH, ANIMAL_HEIGHT)
    cat = pygame.Rect(700, 300, ANIMAL_WIDTH, ANIMAL_HEIGHT)
    dog_bullets = []
    cat_bullets = []
    dog_health = 3
    cat_health = 3
    return dog, cat, dog_bullets, cat_bullets, dog_health, cat_health

def main():
    global SOUND_ENABLED
    
    game_state = MENU
    winner = ""
    
    # Initialize game objects
    dog, cat, dog_bullets, cat_bullets, dog_health, cat_health = reset_game()
    
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                # Global controls
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                # Menu state
                if game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        dog, cat, dog_bullets, cat_bullets, dog_health, cat_health = reset_game()
                    elif event.key == pygame.K_m:
                        SOUND_ENABLED = not SOUND_ENABLED
                
                # Playing state
                elif game_state == PLAYING:
                    # Dog shoots
                    if event.key == pygame.K_LSHIFT and len(dog_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(dog.x + dog.width, dog.y + dog.height//2 - 2, 10, 4)
                        dog_bullets.append(bullet)
                        play_sound(DOG_FIRE_SOUND)
                    
                    # Cat shoots
                    if event.key == pygame.K_RSHIFT and len(cat_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(cat.x, cat.y + cat.height//2 - 2, 10, 4)
                        cat_bullets.append(bullet)
                        play_sound(CAT_FIRE_SOUND)
                
                # Game over state
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        game_state = PLAYING
                        dog, cat, dog_bullets, cat_bullets, dog_health, cat_health = reset_game()
                    elif event.key == pygame.K_m:
                        game_state = MENU
            
            # Handle hits (only during gameplay)
            if game_state == PLAYING:
                if event.type == DOG_HIT:
                    dog_health -= 1
                    play_sound(HIT_SOUND)
                if event.type == CAT_HIT:
                    cat_health -= 1
                    play_sound(HIT_SOUND)
        
        # Game logic
        if game_state == PLAYING:
            # Check for winner
            if dog_health <= 0:
                winner = "Cat Wins!"
                game_state = GAME_OVER
            elif cat_health <= 0:
                winner = "Dog Wins!"
                game_state = GAME_OVER
            else:
                # Move players
                keys = pygame.key.get_pressed()
                move_dog(keys, dog)
                move_cat(keys, cat)
                
                # Handle bullets
                handle_bullets(dog_bullets, cat_bullets, dog, cat)
        
        # Draw based on game state
        if game_state == MENU:
            draw_menu()
        elif game_state == PLAYING:
            draw_game(dog, cat, dog_bullets, cat_bullets, dog_health, cat_health)
        elif game_state == GAME_OVER:
            # Draw the final game state with sleek styling
            WIN.blit(SPACE, (0, 0))
            draw_center_line()
            
            # Draw final health panels
            draw_sleek_ui_panel(WIN, 10, 10, 200, 50, DARK_BLUE, 150)
            dog_health_text = HEALTH_FONT.render(f"Dog Health: {dog_health}", True, NEON_PINK)
            WIN.blit(dog_health_text, (20, 25))
            
            cat_panel_width = 200
            draw_sleek_ui_panel(WIN, WIDTH - cat_panel_width - 10, 10, cat_panel_width, 50, DARK_BLUE, 150)
            cat_health_text = HEALTH_FONT.render(f"Cat Health: {cat_health}", True, LIGHT_BLUE)
            WIN.blit(cat_health_text, (WIDTH - cat_panel_width + 10, 25))
            
            # Draw final player positions
            WIN.blit(DOG_IMAGE, (dog.x, dog.y))
            WIN.blit(CAT_IMAGE, (cat.x, cat.y))
            
            # Draw remaining bullets with glow
            for bullet in dog_bullets:
                glow_surface = pygame.Surface((bullet.width + 4, bullet.height + 4))
                glow_surface.set_alpha(100)
                glow_surface.fill(NEON_PINK)
                WIN.blit(glow_surface, (bullet.x - 2, bullet.y - 2))
                pygame.draw.rect(WIN, NEON_PINK, bullet)
            
            for bullet in cat_bullets:
                glow_surface = pygame.Surface((bullet.width + 4, bullet.height + 4))
                glow_surface.set_alpha(100)
                glow_surface.fill(LIGHT_BLUE)
                WIN.blit(glow_surface, (bullet.x - 2, bullet.y - 2))
                pygame.draw.rect(WIN, LIGHT_BLUE, bullet)
            
            # Draw game over overlay
            draw_game_over(winner)
            pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()