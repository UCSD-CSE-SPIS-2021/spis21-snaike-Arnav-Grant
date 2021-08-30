from tqdm import tqdm
import numpy as np
from genetic_algorithm import *

n_x = 10
n_h = 9
n_h2 = 15
n_y = 4

sol_per_pop = 100
num_weights = n_x * n_h + n_h * n_h2 + n_h2 * n_y

pop_size = (sol_per_pop, num_weights)
# creating a population from scratch
new_population = np.random.choice(np.arange(-1, 1, step = 0.01), size = pop_size, replace = True)
# using old weights
original = np.load('weights_10a_inputs.npy')
clones = np.empty((pop_size[0] - 1, pop_size[1]))
for i in range(clones.shape[0]):
    clones[i, :] = original
modified_original = mutation(clones)
new_population[0, :] = original
new_population[1: , :] = modified_original

num_parents = 12

generations = 1000

for gen in tqdm(range(generations)):
    fitness = cal_pop_fitness(new_population)
    parents = select_mating_pool(new_population, fitness, num_parents)
    offspring_crossover = crossover(parents, offspring_size = (pop_size[0] - parents.shape[0], num_weights))
    offspring_mutation = mutation(offspring_crossover)

    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    best_index = np.where(fitness == np.max(fitness))
    best_index = best_index[0][0]
    np.save('weights_10b_inputs.npy', new_population[best_index])
    # weights = np.load('weights.npy')
    # display_game_with_GA(weights)


# weights1 = np.load('weights_10a_inputs.npy')
# weights2 = np.load('weights_10b_inputs.npy')
# display_game_with_GA(weights1, weights2)


# test_game()
