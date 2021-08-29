import pygame
import os
import random
import numpy as np
from feed_forward_neural_network import *

class Snake:
    def __init__(self, x, y, food):
        self.x = x
        self.y = y
        self.width = 9
        self.height = 9
        self.snake_list = list()
        self.snake_list.append(pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height))
        self.snake_list.append(pygame.Rect((self.x + 1) * 10 + 1, (self.y) * 10 + 1, self.width, self.height))
        self.snake_list.append(pygame.Rect((self.x + 1) * 10 + 1, (self.y + 1) * 10 + 1, self.width, self.height))
        self.state = "none"
        self.food = food

        self.points = 0
        self.vision = 21

        self.map = list()
        self.generate_map()

    def change_directions(self, state):
        # directions = ["left", "right", "up", "down"]
        # left is 0, right is 1, up is 2, down is 3
        if (self.state == 0 and state == 1) or (self.state == 1 and state == 0) or (self.state == 2 and state == 3) or (self.state == 3 and state == 2):
            return
        self.state = state

    def move(self):
        # check if food is in sight
        food_direction = [i for i, x in enumerate(self.observe_all_directions()) if x > 0]
        if len(food_direction) > 0:
            index = food_direction[0]
            reward = 0
            punishment = 5
            if index in [2, 4, 7] and self.state == 3: # up
                self.points += reward
            elif index in [0, 1, 2] and self.state == 0: # right
                self.points += reward
            elif index in [0, 3, 5] and self.state == 2: # down
                self.points += reward
            elif index in [5, 6, 7] and self.state == 1: # left
                self.points += reward
            else:
                self.points -= punishment

        if self.state == 0:
            self.x -= 1
        elif self.state == 1:
            self.x += 1
        elif self.state == 2:
            self.y -= 1
        elif self.state == 3:
            self.y += 1
        else:
            return

        self.snake_list.append((self.x, self.y))

        if self.eat():
            self.points += 1000
            self.food.relocate(self.snake_list)
            return

        self.snake_list.pop(0)

    def generate_map(self):
        for i in range(self.vision):
            self.map.append(list())
            for x in range(self.x - self.vision // 2, self.x + self.vision // 2 + 1):
                y = self.y + i - self.vision // 2

                if x < 0 or x > grid_width - 1 or y < 0 or y > grid_height - 1:
                    self.map[i].append(-1)
                elif self.food.x == x and self.food.y == y:
                    self.map[i].append(2)
                elif (x, y) in self.snake_list:
                    self.map[i].append(1)
                else:
                    self.map[i].append(0)

    def flatten_map(self):
        li = list()
        for i in self.map:
            li += i

        return li

    def observe(self):
        return self.flatten_map()

    def eat(self):
        if self.x == self.food.x and self.y == self.food.y:
            return True
        else:
            return False

    def draw(self):
        for segment in self.snake_list:
            pygame.draw.rect(screen, (77, 237, 48), pygame.Rect(segment[0] * 10 + 1, segment[1] * 10 + 1, self.width, self.height))

    def dead(self):
        punishment = 900

        if self.x < 0 or self.x >= grid_width or self.y < 0 or self.y >= grid_height:
            self.points -= punishment
            return True
        elif self.collide_body():
            self.points -= punishment
            return True
        else:
            return False

    def collide_body(self):
        for segment in self.snake_list[:-1]:
            if segment[0] == self.x and segment[1] == self.y:
                return True

        return False

    def observe(self):
        return self.observe_all_directions() + self.apple_direction()

    def observe_all_directions(self):
        # Observe what is happening in each of the 8 directions from the snake
        # For each of the 8 directions, find out the distance between the snake and the food, wall, and body
        observations = list()

        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                if x_dir == 0 and y_dir == 0:
                    continue
                observations += self.observe_direction(x_dir, y_dir)

        return observations

    def observe_direction(self, x_dir, y_dir):
        x_bounds = -1 if x_dir < 0 else grid_width
        y_bounds = -1 if y_dir < 0 else grid_height
        x = self.x
        y = self.y

        dist_covered = 0
        (dist_food, dist_wall, dist_body) = (-1, -1, -1)

        body_hit = False

        while x != x_bounds and y != y_bounds:
            x += x_dir
            y += y_dir
            dist_covered += 1

            if x == self.food.x and y == self.food.y:
                dist_food = dist_covered
            if x == x_bounds or y == y_bounds:
                dist_wall = dist_covered
            if not body_hit:
                for segment in self.snake_list[:-1]:
                    if segment[0] == self.x and segment[1] == self.y:
                        dist_body = dist_covered
                        body_hit = True
                        break

        dist_obstacle = dist_wall if dist_body < 0 else min(dist_body, dist_wall)

        return [dist_food if dist_food < dist_obstacle and dist_food > 0 else -dist_obstacle]

    def apple_direction(self):
        vector = list()
        x_diff = self.food.x - self.x
        y_diff = self.food.y - self.y

        if x_diff != 0:
            vector.append(int(abs(x_diff) / x_diff))
        else:
            vector.append(0)

        if y_diff != 0:
            vector.append(int(abs(y_diff) / y_diff))
        else:
            vector.append(0)

        return vector

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.x = random.randint(0, self.grid_width - 1)
        self.y = random.randint(0, self.grid_height - 1)
        self.width = 9
        self.height = 9
        self.rect = pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height)

    def relocate(self, snake):
        self.x = random.randint(0, self.grid_width - 1)
        self.y = random.randint(0, self.grid_height - 1)
        self.rect = pygame.Rect(self.x * 10 + 1, self.y * 10 + 1, self.width, self.height)
        if (self.x, self.y) in snake:
            self.relocate(snake)

    def draw(self):
        pygame.draw.rect(screen, (218, 165, 32), self.rect)

def display_game_with_GA(weights):
    f = Food(grid_width, grid_height)

    player = Snake(random.randint(1, grid_width - 2), random.randint(1, grid_height - 2), f)

    max_steps = 3000
    running = True
    for i in range(max_steps):
        pygame.event.get()
        clock.tick(FPS)

        for event in pygame.event.get():
        # If you press the x button on the top right, quit the game
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
            # If you press the q key, quit the game
                if event.key == pygame.K_q:
                    running = False

        if not running:
            break

        # player.change_directions(random.randint(0, 3))
        predicted_direction = np.argmax(np.array(forward_propagation(np.array(player.observe()).reshape(-1, n_x), weights)))
        print(np.array(forward_propagation(np.array(player.observe()).reshape(-1, n_x), weights)))
        print(predicted_direction)
        player.change_directions(predicted_direction)

        player.move()

        if player.dead():
            break

        pygame.draw.rect(screen, (0, 0, 0), background)
        player.draw()
        player.food.draw()
        pygame.display.update()

    return player.points

def run_game_with_GA(weights):
    f = Food(grid_width, grid_height)

    player = Snake(random.randint(1, grid_width - 2), random.randint(1, grid_height - 2), f)

    max_steps = 3000
    for i in range(max_steps):
        pygame.event.get()
        # player.change_directions(random.randint(0, 3))
        predicted_direction = np.argmax(np.array(forward_propagation(np.array(player.observe()).reshape(-1, n_x), weights))) % 4
        player.change_directions(predicted_direction)

        player.move()

        if player.dead():
            break

        pygame.draw.rect(screen, (0, 0, 0), background)
        player.draw()
        player.food.draw()
        pygame.display.update()

    return player.points

def test_game():
    f = Food(grid_width, grid_height)

    player = Snake(random.randint(1, grid_width - 2), random.randint(1, grid_height - 2), f)

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
                if event.key == pygame.K_w:
                    player.change_directions(2)
                if event.key == pygame.K_s:
                    player.change_directions(3)
                if event.key == pygame.K_a:
                    player.change_directions(0)
                if event.key == pygame.K_d:
                    player.change_directions(1)

        # directions = ["left", "right", "up", "down"]
        player.move()

        player.observe()

        if player.dead():
            running = False
            continue

        pygame.draw.rect(screen, (0, 0, 0), background)
        player.draw()
        player.food.draw()
        pygame.display.update()

        # print(player.observe())
        print(player.observe())
    else:
        print("You lose! Your snake's length was " + str(len(player.snake_list)))

# These are the dimensions of the background image for our game
(grid_width, grid_height) = (40, 40)
screen_length = grid_width * 10 + 1
screen_height = grid_height * 10 + 1
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)

background = pygame.Rect(0, 0, screen_length, screen_height)

FPS = 10

# Game loop
clock = pygame.time.Clock()
# Direction travelling
# each of the 8 directions from the snake
# location of apple
