import pygame
import os
import random
import 

class Snake:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = 9
    self.height = 9
    self.snake_list = list()
    self.snake_list.append(pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height))

    self.x_dir = 0
    self.y_dir = 0
  
  def change_directions(self, dx, dy):
    self.x_dir = dx
    self.y_dir = dy

  def move(self):
    self.x += self.x_dir
    self.y += self.y_dir
    self.snake_list.append(pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height))

    if self.eat(food):
      food.relocate()
      return
    
    self.snake_list.pop(0)
    
  def eat(self, food):
    if self.x == food.x and self.y == food.y:
      return True
    else:
      return False

  def draw(self):
    for segment in self.snake_list:
      pygame.draw.rect(screen, (77, 237, 48), segment)
  
  def dead(self):
    if self.x < 0 or self.x >= grid_width or self.y < 0 or self.y >= grid_height:
      return True
    elif self.collide_body():
      # Hit own body
      return True
    else:
      return False
  
  def collide_body(self):
    for segment in self.snake_list[:-1]:
      if (segment.left - 1) / 10 == self.x and (segment.top - 1) / 10 == self.y:
        return True
    
    return False

class Food:
  def __init__(self, grid_width, grid_height):
    self.grid_width = grid_width
    self.grid_height = grid_height
    self.x = random.randint(0, self.grid_width)
    self.y = random.randint(0, self.grid_height)
    self.width = 9
    self.height = 9
    self.rect = pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height)
  
  def relocate(self):
    self.x = random.randint(0, self.grid_width - 1)
    self.y = random.randint(0, self.grid_height - 1)
    self.rect = pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height)
    print(self.x, self.y)
  
  def draw(self):
    pygame.draw.rect(screen, (218, 165, 32), self.rect)

# These are the dimensions of the background image for our game
(grid_width, grid_height) = (30, 30)
screen_length = grid_width * 10 + 1
screen_height = grid_height * 10 + 1
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)

background = pygame.Rect(0, 0, screen_length, screen_height)

# Player variables
player = Snake(1, 1)

# Food variables
food = Food(grid_width, grid_height)
food.relocate()

FPS = 10

# Game loop
clock = pygame.time.Clock()
running = True
while running:
  clock.tick(FPS)

  for event in pygame.event.get():
    # If you press the x button on the top right, quit the game
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      # If you press the q key, quit the game
      if event.key == pygame.K_q:
        running = False
      elif event.key == pygame.K_w:
        player.change_directions(0, -1)
      elif event.key == pygame.K_s:
        player.change_directions(0, 1)
      elif event.key == pygame.K_a:
        player.change_directions(-1, 0)
      elif event.key == pygame.K_d:
        player.change_directions(1, 0)

  player.move()

  if player.dead():
    running = False
    continue
  
  pygame.draw.rect(screen, (0, 0, 0), background)
  player.draw()
  food.draw()
  pygame.display.update()
else:
  print("You lose! Your snake's length was " + str(len(player.snake_list)))

# Direction travelling
# each of the 8 directions from the snake
# location of apple