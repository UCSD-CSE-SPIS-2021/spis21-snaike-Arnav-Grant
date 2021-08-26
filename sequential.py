from snake import *
from tqdm import tqdm
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# # Food variables
# f = Food(grid_width, grid_height)
# f.relocate()
#
# # Player variables
# player = Snake(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), f)
#
#
#
# play_game(player)

def generate_training_data():
    training_data_inputs = list()
    training_data_outputs = list()
    training_games = 2500
    steps_per_game = 2000

    for _ in tqdm(range(training_games)):
        # initialize a game
        f = Food(grid_width, grid_height)
        f.relocate()

        player = Snake(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), f)

        for _ in range(steps_per_game):
            direction = random.randint(0, 3)
            player.change_directions(direction)
            output = [0, 0, 0, 0]
            output[direction] = 1

            player.move()

            if player.dead():
                break

            training_data_outputs.append(output)
            training_data_inputs.append(player.observe())

    return training_data_inputs, training_data_outputs

def run_game_with_model(model):
    f = Food(grid_width, grid_height)
    f.relocate()

    player = Snake(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), f)

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

        # player.change_directions(random.randint(0, 3))
        predicted_direction = np.argmax(np.array(model.predict(np.array(player.observe()).reshape(-1, n_x))))
        print(predicted_direction)
        player.change_directions(predicted_direction)


        player.move()

        if player.dead():
            running = False
            continue

        pygame.draw.rect(screen, (0, 0, 0), background)
        player.draw()
        player.food.draw()
        pygame.display.update()

        # print(player.observe())
    else:
        print("You lose! Your snake's length was " + str(len(player.snake_list)))

n_x = 24
n_h = 9
n_h2 = 15
n_y = 4

(data_inputs, data_outputs) = generate_training_data()
print(len(data_inputs), len(data_outputs))

model = keras.Sequential()
model.add(keras.Input(shape = (n_x,)))
model.add(layers.Dense(units = n_h, activation = "relu"))
model.add(layers.Dense(units = n_h2, activation = "relu"))
model.add(layers.Dense(units = n_y, activation = "softmax"))

model.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["accuracy"])
model.fit((np.array(data_inputs).reshape(-1, n_x)), (np.array(data_outputs).reshape(-1, n_y)), batch_size = 256, epochs = 3)

run_game_with_model(model)

# generate training (inputs: each of 8 directions) (outputs: direction it moves (random))
# shove this training data into a model
# create some instance of a snake and then we run tests on this snake after mutating it
# genetic algorithm
