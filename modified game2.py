import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASKET_WIDTH, BASKET_HEIGHT = 100, 20
SQUARE_SIZE = 30
GAME_DURATION = 60  # seconds

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Square Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BASKET_WIDTH, BASKET_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 20)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class FallingSquare(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, WIDTH - SQUARE_SIZE), 0)

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.topleft = (random.randint(0, WIDTH - SQUARE_SIZE), 0)

def game_loop():
    all_sprites = pygame.sprite.Group()
    baskets = pygame.sprite.Group()
    squares = pygame.sprite.Group()

    basket = Basket()
    all_sprites.add(basket)
    baskets.add(basket)

    score = 0
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()

        # Check for collisions
        collisions = pygame.sprite.spritecollide(basket, squares, True)
        for _ in collisions:
            score += 1
            square = FallingSquare()
            all_sprites.add(square)
            squares.add(square)

        # Generate a new FallingSquare every second
        if pygame.time.get_ticks() % 1000 == 0:
            square = FallingSquare()
            all_sprites.add(square)
            squares.add(square)

        # Draw background
        screen.fill(BLACK)

        # Draw sprites
        all_sprites.draw(screen)

        # Display remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, GAME_DURATION - elapsed_time)
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {remaining_time}", True, WHITE)
        screen.blit(time_text, (10, 10))

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))

        # Update display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(FPS)

        # Check for game over condition
        if elapsed_time >= GAME_DURATION:
            break

    # Display game over screen
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render(f"Game Over! Your Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display game over screen for 3 seconds before quitting

if __name__ == "__main__":
    game_loop()