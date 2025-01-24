import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLOB_COLOR = (200, 200, 200)  # A slightly gray white for better visibility

# Bird properties
bird_width = 40
bird_height = 40
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5

# Pipe properties
pipe_width = 70
pipe_gap = 200
pipe_velocity = 3

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(50, SCREEN_HEIGHT - pipe_gap - 150)
        self.passed = False

    def move(self):
        self.x -= pipe_velocity

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, pipe_width, self.height))  # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + pipe_gap, pipe_width, SCREEN_HEIGHT - self.height - pipe_gap))  # Bottom pipe

class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 3  # Blob falls down

    def move(self):
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, BLOB_COLOR, (int(self.x), int(self.y)), 10)  # Draw a circle for the blob

def game_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Press any key to start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True

pipes = []
blobs = []  # List to hold all blobs
score = 0

# Main game loop
if game_start_screen():
    running = True
    clock = pygame.time.Clock()

    pipes.append(Pipe())  # Initialize with one pipe

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -10  # Jump up
                    # Add a new blob when the bird flaps
                    blobs.append(Blob(bird_x + bird_width // 2, bird_y + bird_height))

        # Move the bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Check for collisions
        if bird_y > SCREEN_HEIGHT - bird_height or bird_y < 0:
            running = False
        
        pipes_to_remove = []
        for pipe in pipes:
            if pipe.x < bird_x < pipe.x + pipe_width:
                if bird_y < pipe.height or bird_y + bird_height > pipe.height + pipe_gap:
                    running = False
            if not pipe.passed and pipe.x < bird_x:
                pipe.passed = True
                score += 1

            pipe.move()
            if pipe.x + pipe_width < 0:
                pipes_to_remove.append(pipe)

        # Move and remove blobs that are off-screen
        blobs_to_remove = []
        for blob in blobs:
            blob.move()
            if blob.y > SCREEN_HEIGHT:
                blobs_to_remove.append(blob)

        for blob in blobs_to_remove:
            blobs.remove(blob)

        # Remove pipes that are off screen
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # Add new pipe
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 300:
            pipes.append(Pipe())

        # Draw everything
        screen.fill(WHITE)
        for pipe in pipes:  # Draw pipes before bird, blobs, and score
            pipe.draw()
        for blob in blobs:  # Draw blobs after pipes
            blob.draw()
        pygame.draw.rect(screen, BLACK, (bird_x, bird_y, bird_width, bird_height))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

pygame.quit()
