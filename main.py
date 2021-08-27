from tqdm import tqdm
import numpy as np
from genetic_algorithm import *

n_x = 8
n_h = 9
n_h2 = 15
n_y = 4

sol_per_pop = 250
num_weights = n_x * n_h + n_h * n_h2 + n_h2 * n_y

pop_size = (sol_per_pop, num_weights)
new_population = np.random.choice(np.arange(-1, 1, step = 0.01), size = pop_size, replace = True)

num_parents = 12

generations = 50

for gen in tqdm(range(generations)):
    fitness = cal_pop_fitness(new_population)
    parents = select_mating_pool(new_population, fitness, num_parents)
    offspring_crossover = crossover(parents, offspring_size = (pop_size[0] - parents.shape[0], num_weights))
    offspring_mutation = mutation(offspring_crossover)

    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    if gen % 5 == 0 or gen == generations - 1:
        f = open("best_weights.txt", "w")
        best_index = np.where(fitness == np.max(fitness))
        best_index = best_index[0][0]
        f.write(str(new_population[best_index]))

        f = open("best_weights.txt", "r")
        x = f.read()
        x = x.replace("\n", "").replace("[", "").replace("]", "")
        li = x.split()
        weights = [float(s) for s in li]
        display_game_with_GA(np.array(weights))


# test_game()
