from tqdm import tqdm
import numpy as np
from genetic_algorithm import *

n_x = 10
n_h = 9
n_h2 = 15
n_y = 4

sol_per_pop = 200
size_per_game = 10
num_weights = n_x * n_h + n_h * n_h2 + n_h2 * n_y

pop_size = (sol_per_pop, num_weights)
# creating a population from scratch
new_population = np.random.choice(np.arange(-1, 1, step = 0.01), size = pop_size, replace = True)

# using old weights -- OLD
# original = np.load('weights_10a_inputs.npy')
# clones = np.empty((pop_size[0] - 1, pop_size[1]))
# for i in range(clones.shape[0]):
#     clones[i, :] = original
# modified_original = mutation(clones)
# new_population[0, :] = original
# new_population[1: , :] = modified_original

# using old weights -- NEW
# originals = np.empty((size_per_game, pop_size[1]))
# for i in range(size_per_game):
#     weights = np.load('weights/weights_deathmatch_test_' + str(i) + '.npy')
#     originals[i, :] = weights
# originals_crossover = crossover(originals, offspring_size = (pop_size[0] - originals.shape[0], num_weights))
# originals_mutation = mutation(originals_crossover)
# new_population[0: originals.shape[0], :] = originals
# new_population[originals.shape[0]:, :] = originals_mutation



num_parents = 12

generations = 5000

# for gen in tqdm(range(generations)):
#     fitness = cal_pop_fitness(new_population, size_per_game)
#     parents = select_mating_pool(new_population, fitness, num_parents)
#     offspring_crossover = crossover(parents, offspring_size = (pop_size[0] - parents.shape[0], num_weights))
#     offspring_mutation = mutation(offspring_crossover)
#
#     new_population[0:parents.shape[0], :] = parents
#     new_population[parents.shape[0]:, :] = offspring_mutation
#
#     best = select_mating_pool(new_population, fitness, size_per_game)
#     for i in range(len(best)):
#         np.save('weights/weights_deathmatch_test_' + str(i) + '.npy', best[i])


# weights = np.load('weights/weights_deathmatch_0.npy')
originals = np.empty((size_per_game, pop_size[1]))
for i in range(size_per_game):
    weights = np.load('weights/weights_deathmatch_test_' + str(i) + '.npy')
    originals[i, :] = weights
display_game_with_GA(originals, size_per_game)

# test_game()
