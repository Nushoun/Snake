import pygame
import random
from pygame.locals import *

pygame.init()
# Screen dimensions and grid settings
width = 800
height = 800
grid_pixels = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
point = 0
GAME_PLAYING = True
GAME_OVER = False
game_state = GAME_PLAYING
game_paused = False
# Colors
background_color = (0, 0, 0)
grid_color = (90, 200, 200)
snake_color = (0, 255, 0)
apple_color = (250, 0, 0)

# Grid initialization
grid = []
for row in range(height // grid_pixels):
    for col in range(width // grid_pixels):
        x = col * grid_pixels
        y = row * grid_pixels
        rect = pygame.Rect(x, y, grid_pixels, grid_pixels)
        grid.append(rect)

random_grid = random.choice(grid)

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = grid_pixels
        self.height = grid_pixels
        random_grid = random.choice(grid)
        self.x = random_grid.x
        self.y = random_grid.y
        self.color = snake_color
        self.vel = grid_pixels
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.direction = pygame.K_RIGHT
        self.list = [[self.x, self.y]]
        self.lenght = 1

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.direction != pygame.K_RIGHT:
            self.direction = pygame.K_LEFT
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.direction != pygame.K_LEFT:
            self.direction = pygame.K_RIGHT
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.direction != pygame.K_DOWN:
            self.direction = pygame.K_UP
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.direction != pygame.K_UP:
            self.direction = pygame.K_DOWN

        if self.direction == pygame.K_LEFT:
            self.x -= self.vel
        elif self.direction == pygame.K_RIGHT:
            self.x += self.vel
        elif self.direction == pygame.K_UP:
            self.y -= self.vel
        elif self.direction == pygame.K_DOWN:
            self.y += self.vel

        if self.x < 0:
            self.x = 0
        elif self.x >= width:
            self.x = width - grid_pixels
        if self.y < 0:
            self.y = 0
        elif self.y >= height:
            self.y = height - grid_pixels

        self.list.append([self.x, self.y])
        if len(self.list) > self.lenght:
            del self.list[0]

    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.image.fill(self.color)
        for part in self.list:
            pygame.draw.rect(screen, self.color, pygame.Rect(part[0], part[1], self.width, self.height))
        new_head = [self.x, self.y]
        if self.list.count(new_head) > 1:
                game_over()

class apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = grid_pixels
        self.height = grid_pixels
        self.x = random_grid.x
        self.y = random_grid.y
        self.color = apple_color
        self.vel = grid_pixels
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.respawn()

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def respawn(self):
        while True:    
            random_grid =random.choice(grid)
            self.x = random_grid.x
            self.y = random_grid.y
            self.rect.topleft = (self.x, self.y)
            if [self.x, self.y] not in snek.list:
                break
        self.rect.topleft = (self.x, self.y)

def score():
    font = pygame.font.Font(None, 50)
    color = ("white")
    text = font.render(str(point), True, color)
    screen.blit(text, (20, 20))

def game_over():
    print("GAME OVER")
    global game_state, game_paused
    game_state = GAME_OVER
    game_paused = True

def pauser_menu():
    font = pygame.font.Font(None, 100)
    color = (255, 0, 0)
    text = font.render("Game Over", True, color)
    screen.blit(text, (width // 4, height // 2 - 50))
    font = pygame.font.Font(None, 80)
    text = font.render("Press SPACE to restart", True, "white")
    screen.blit(text, (width // 6, height // 2 + 50))
    snek.lenght = 1
    snek.list.clear()
    snake_group.empty()
    fruit_group.empty()
    pygame.display.update()

def resume():
    global game_paused, game_state, point, snek, fruit
    respawn()
    game_paused = False
    game_state = GAME_PLAYING
    point = 0
    pygame.display.update()
    print("RESUME")

def respawn():
    snek.x = random_grid.x
    snek.y = random_grid.y
    snake_group.add(snek)
    fruit_group.add(fruit)
    snake_group.update()
    fruit_group.update()
    print("RESPAWN")

# Create snake and fruit object groups
snek = Snake()
snake_group = pygame.sprite.Group()
snake_group.add(snek)

fruit = apple()
fruit_group = pygame.sprite.Group()
fruit_group.add(fruit)

# Main game loop
run = True
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == GAME_OVER:
                resume()
    if game_state == GAME_PLAYING:
        screen.fill(background_color)
        for rect in grid:
            pygame.draw.rect(screen, grid_color, rect, 1)       
        score()
        snek.move()                                             #Movement
        snake_group.update()                                    #spawn
        fruit_group.draw(screen)
        fruit_group.update()

        collide = pygame.sprite.groupcollide(snake_group, fruit_group, False, False)
        if collide:
            fruit.respawn()
            point += 1
            snek.lenght += 1
            print("point")
        pygame.display.update()
        clock.tick(10)  # Control the frame rate
    else:
        if game_state == GAME_OVER:
            pauser_menu()
        elif game_state  == GAME_PLAYING:
            continue

pygame.quit()
