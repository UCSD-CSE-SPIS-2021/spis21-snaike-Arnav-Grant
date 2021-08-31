import pygame
import os
import random
import numpy as np
from feed_forward_neural_network import *
import math

class Snake:
    def __init__(self, x, y, foods, color):
        self.x = x
        self.y = y
        self.width = 9
        self.height = 9
        self.snake_list = list()
        self.snake_list.append((self.x + 1, self.y + 1))
        self.snake_list.append((self.x + 1, self.y))
        self.snake_list.append((self.x, self.y))
        self.state = "none"
        self.foods = foods
        self.color = color
        self.isDead = False

        self.points = 0

    def change_directions(self, state):
        # directions = ["left", "right", "up", "down"]
        # left is 0, right is 1, up is 2, down is 3
        if (self.state == 0 and state == 1) or (self.state == 1 and state == 0) or (self.state == 2 and state == 3) or (self.state == 3 and state == 2):
            return
        self.state = state

    def move(self):
        # check if food is in sight
        # food_direction = [i for i, x in enumerate(self.observe_all_directions(list())) if x > 0]
        # if len(food_direction) > 0:
        #     index = food_direction[0]
        #     reward = 0
        #     punishment = 5
        #     if index in [2, 4, 7] and self.state == 3: # down
        #         self.points += reward
        #     elif index in [0, 1, 2] and self.state == 0: # right
        #         self.points += reward
        #     elif index in [0, 3, 5] and self.state == 2: # up
        #         self.points += reward
        #     elif index in [5, 6, 7] and self.state == 1: # left
        #         self.points += reward
        #     else:
        #         self.points -= punishment

        apple_vector = self.apple_direction()
        punishment = 20
        if apple_vector[0] < 0 and self.state == 1:
            self.points -= punishment
        elif apple_vector[0] > 0 and self.state == 0:
            self.points -= punishment
        elif apple_vector[0] == 0 and (self.state == 3 or self.state == 2):
            self.points -= punishment

        if apple_vector[1] < 0 and self.state == 3:
            self.points -= punishment
        elif apple_vector[1] > 0 and self.state == 2:
            self.points -= punishment
        elif apple_vector[1] == 0 and (self.state == 1 or self.state == 0):
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

        eaten = self.eat()
        if eaten:
            self.points += 1100
            eaten.relocate(self.snake_list)
            return

        self.snake_list.pop(0)

    def eat(self):
        for food in self.foods:
            if self.x == food.x and self.y == food.y:
                return food

        return None

    def draw(self):
        for segment in self.snake_list:
            pygame.draw.rect(screen, self.color, pygame.Rect(segment[0] * 10 + 1, segment[1] * 10 + 1, self.width, self.height))

    def dead(self, snakes):
        punishment = 900

        if self.x < 0 or self.x >= grid_width or self.y < 0 or self.y >= grid_height:
            self.points -= punishment
            self.isDead = True
            return True
        elif self.collide_body():
            self.points -= punishment
            self.isDead = True
            return True
        elif self.collide_other(snakes):
            self.points -= punishment
            self.isDead = True
            return True
        else:
            return False

    def collide_body(self):
        for segment in self.snake_list[:-1]:
            if segment[0] == self.x and segment[1] == self.y:
                return True

        return False

    def collide_other(self, snakes):
        for snake in snakes:
            if (self.x, self.y) in snake.snake_list:
                return True
        return False

    def observe(self, snakes):
        return self.observe_all_directions(snakes) + self.apple_direction()

    def observe_all_directions(self, snakes):
        # Observe what is happening in each of the 8 directions from the snake
        # For each of the 8 directions, find out the distance between the snake and the food, wall, and body
        observations = list()

        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                if x_dir == 0 and y_dir == 0:
                    continue
                observations += self.is_blocked(x_dir, y_dir, snakes)

        return observations

    def is_blocked(self, x_dir, y_dir, snakes):
        x_bounds = -1 if x_dir < 0 else grid_width
        y_bounds = -1 if y_dir < 0 else grid_height
        x = self.x + x_dir
        y = self.y + y_dir

        for snake in snakes:
            if (x, y) in snake.snake_list:
                return [1]
        if x == x_bounds or y == y_bounds:
            return [1]
        if (x, y) in self.snake_list[:-1]:
            return [1]

        return [0]

    # def observe_direction(self, x_dir, y_dir, snakes):
    #     x_bounds = -1 if x_dir < 0 else grid_width
    #     y_bounds = -1 if y_dir < 0 else grid_height
    #     x = self.x
    #     y = self.y
    #
    #     dist_covered = 0
    #
    #     while x != x_bounds and y != y_bounds:
    #         x += x_dir
    #         y += y_dir
    #         dist_covered += 1
    #
    #         if x == self.food.x and y == self.food.y:
    #             # if self.color == (255, 255, 255):
    #             #     print("x_dir:", x_dir, ", y_dir:", y_dir, ", Food", dist_covered)
    #             return [dist_covered]
    #         for snake in snakes:
    #             if (x, y) in snake.snake_list:
    #                 # if self.color == (255, 255, 255):
    #                 #     print("x_dir:", x_dir, ", y_dir:", y_dir, ", Enemy", dist_covered)
    #                 return [-dist_covered]
    #         if x == x_bounds or y == y_bounds:
    #             # if self.color == (255, 255, 255):
    #             #     print("x_dir:", x_dir, ", y_dir:", y_dir, ", Wall", dist_covered)
    #             return [-dist_covered]
    #         if (x, y) in self.snake_list[:-1]:
    #             # if self.color == (255, 255, 255):
    #             #     print("x_dir:", x_dir, ", y_dir:", y_dir, ", Body", dist_covered)
    #             return [-dist_covered]

    def apple_direction(self):
        vector = list()
        distances = [self.dist(f) for f in self.foods]
        closest_food = self.foods[distances.index(min(distances))]
        x_diff = closest_food.x - self.x
        y_diff = closest_food.y - self.y

        vector.append(x_diff)
        vector.append(y_diff)

        return vector

    def dist(self, food):
        return math.sqrt((food.x - self.x) ** 2 + (food.y - self.y) ** 2)

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
        # if (self.x, self.y) in snake:
        #     self.relocate(snake)

    def draw(self):
        pygame.draw.rect(screen, (218, 165, 32), self.rect)

def display_game_with_GA(weights, num_snakes):
    f = [Food(grid_width, grid_height), Food(grid_width, grid_height), Food(grid_width, grid_height)]

    player_list = list()

    for i in range(num_snakes):
        player_list.append(Snake(random.randint(1, grid_width - 2), random.randint(1, grid_height - 2), f, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    max_steps = 2000
    running = True
    for i in range(max_steps):
        pygame.event.get()
        clock.tick(FPS)

        alive_list = [snek for snek in player_list if not snek.isDead]

        if len(alive_list) == 0:
            running = False

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

        for i in range(len(alive_list)):
            player = alive_list[i]
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(player.observe(alive_list[0: i] + alive_list[i + 1: len(alive_list)])).reshape(-1, n_x), weights[i])))
            player.change_directions(predicted_direction)
            player.move()

        for i in range(len(alive_list)):
            player = alive_list[i]
            if not player.isDead and player.dead(alive_list[0: i] + alive_list[i + 1: len(alive_list)]):
                continue

        pygame.draw.rect(screen, (0, 0, 0), background)
        for player in alive_list:
            if not player.isDead:
                player.draw()
        for f in alive_list[0].foods:
            f.draw()
        pygame.display.update()

    for i in range(len(player_list)):
        print("Player " + str(i) + " was " + str(len(player_list[i].snake_list)) + " long!")

def run_game_with_GA(weights, num_snakes):
    f = [Food(grid_width, grid_height), Food(grid_width, grid_height), Food(grid_width, grid_height)]

    player_list = list()

    for i in range(num_snakes):
        player_list.append(Snake(random.randint(1, grid_width - 2), random.randint(1, grid_height - 2), f, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    max_steps = 2000
    for i in range(max_steps):
        pygame.event.get()

        alive_list = [snek for snek in player_list if not snek.isDead]

        if len(alive_list) == 0:
            break

        for i in range(len(alive_list)):
            player = alive_list[i]
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(player.observe(alive_list[0: i] + alive_list[i + 1: len(alive_list)])).reshape(-1, n_x), weights[i])))
            player.change_directions(predicted_direction)
            player.move()

        for i in range(len(alive_list)):
            player = alive_list[i]
            if not player.isDead and player.dead(alive_list[0: i] + alive_list[i + 1: len(alive_list)]):
                continue

        pygame.draw.rect(screen, (0, 0, 0), background)
        for player in alive_list:
            if not player.isDead:
                player.draw()
        for f in alive_list[0].foods:
            f.draw()
        pygame.display.update()

    scores = [player.points for player in player_list]

    return scores

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

        if player.dead():
            running = False
            continue

        pygame.draw.rect(screen, (0, 0, 0), background)
        player.draw()
        player.food.draw()
        pygame.display.update()

        # print(player.observe())
        print(player.observe(player2))
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
