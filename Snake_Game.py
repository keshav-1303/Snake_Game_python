import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize font
font = pygame.font.SysFont(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = (1, 0)  # Start moving right
        self.color = GREEN
        self.head_color = DARK_GREEN
        self.score = 0
        self.growth_pending = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_position = (
            (head_x + direction_x) % GRID_WIDTH,
            (head_y + direction_y) % GRID_HEIGHT
        )
        
        # Game over if snake hits itself
        if new_position in self.positions[1:]:
            return True  # Game over
        
        self.positions.insert(0, new_position)
        
        # Handle growth
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.positions.pop()
            
        return False  # Game continues

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = self.head_color if i == 0 else self.color
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
            # Draw eyes on the head
            if i == 0:
                # Determine eye positions based on direction
                direction_x, direction_y = self.direction
                # Base eye positions
                eye_radius = GRID_SIZE // 8
                
                # Adjust eye positions based on direction
                if direction_x == 1:  # Right
                    eye_pos1 = (rect.x + 3*rect.width//4, rect.y + rect.height//4)
                    eye_pos2 = (rect.x + 3*rect.width//4, rect.y + 3*rect.height//4)
                elif direction_x == -1:  # Left
                    eye_pos1 = (rect.x + rect.width//4, rect.y + rect.height//4)
                    eye_pos2 = (rect.x + rect.width//4, rect.y + 3*rect.height//4)
                elif direction_y == 1:  # Down
                    eye_pos1 = (rect.x + rect.width//4, rect.y + 3*rect.height//4)
                    eye_pos2 = (rect.x + 3*rect.width//4, rect.y + 3*rect.height//4)
                else:  # Up
                    eye_pos1 = (rect.x + rect.width//4, rect.y + rect.height//4)
                    eye_pos2 = (rect.x + 3*rect.width//4, rect.y + rect.height//4)
                
                pygame.draw.circle(surface, WHITE, eye_pos1, eye_radius)
                pygame.draw.circle(surface, WHITE, eye_pos2, eye_radius)
                pygame.draw.circle(surface, BLACK, eye_pos1, eye_radius // 2)
                pygame.draw.circle(surface, BLACK, eye_pos2, eye_radius // 2)

    def change_direction(self, direction):
        # Prevent 180-degree turns (can't go opposite direction)
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow(self):
        self.growth_pending += 1
        self.score += 1


class Apple:
    def __init__(self, snake_positions):
        self.position = self.get_random_position(snake_positions)
        self.color = RED

    def get_random_position(self, snake_positions):
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        # Ensure apple doesn't spawn on snake
        while position in snake_positions:
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
        return position

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        # Draw stem
        stem_rect = pygame.Rect(
            self.position[0] * GRID_SIZE + GRID_SIZE // 2 - 1,
            self.position[1] * GRID_SIZE - GRID_SIZE // 6,
            2, GRID_SIZE // 4
        )
        pygame.draw.rect(surface, DARK_GREEN, stem_rect)
        
        # Draw leaf
        leaf_points = [
            (self.position[0] * GRID_SIZE + GRID_SIZE // 2 + 2, 
             self.position[1] * GRID_SIZE - GRID_SIZE // 8),
            (self.position[0] * GRID_SIZE + GRID_SIZE // 2 + 6, 
             self.position[1] * GRID_SIZE - GRID_SIZE // 4),
            (self.position[0] * GRID_SIZE + GRID_SIZE // 2 + 2, 
             self.position[1] * GRID_SIZE - GRID_SIZE // 3)
        ]
        pygame.draw.polygon(surface, DARK_GREEN, leaf_points)


def draw_grid(surface):
    # Draw a subtle checkerboard pattern instead of grid lines
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            if (x + y) % 2 == 0:
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, (20, 20, 20), rect)


def game_over_screen(surface, score):
    surface.fill(BLACK)
    
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to play again", True, WHITE)
    quit_text = font.render("Press ESC to quit", True, WHITE)
    
    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)
    
    return False


def show_start_screen(surface):
    surface.fill(BLACK)
    
    title_text = font.render("SNAKE GAME", True, GREEN)
    instruction_text = font.render("Use arrow keys to move", True, WHITE)
    start_text = font.render("Press SPACE to start", True, YELLOW)
    
    surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 60))
    surface.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)


def main():
    show_start_screen(screen)
    
    snake = Snake()
    apple = Apple(snake.positions)
    
    running = True
    game_over = False
    current_fps = FPS
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        if not game_over:
            # Update game state
            game_over = snake.update()
            
            # Check if snake ate the apple
            if snake.get_head_position() == apple.position:
                snake.grow()
                apple = Apple(snake.positions)
                
                # Increase speed every 5 points
                if snake.score % 5 == 0 and current_fps < 20:
                    current_fps += 1
            
            # Check if snake hit the wall (game over)
            head_x, head_y = snake.get_head_position()
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                game_over = True
            
            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)  # This now draws a subtle checkerboard pattern
            apple.draw(screen)
            snake.draw(screen)  # Draw snake after apple so it appears on top
            
            # Draw score
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            pygame.display.update()
            
            if game_over:
                time.sleep(0.5)  # Brief pause before game over screen
                if game_over_screen(screen, snake.score):
                    # Restart game
                    return main()
                else:
                    running = False
        
        clock.tick(current_fps)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()