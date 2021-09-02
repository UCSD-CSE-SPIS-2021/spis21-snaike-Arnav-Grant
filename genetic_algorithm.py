# Shamelessly stolen from the following link:
# https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm/blob/master/Genetic_Algorithm.py

import random
from snake import *
from feed_forward_neural_network import *
import numpy as np
from tqdm import tqdm

def cal_pop_fitness(pop):
    # create a list of fitness for each snake
    fitness = []
    # iterate through all the snakes in the population
    for i in range(pop.shape[0]):
        # run a simulation with the feed forward neural network and record the fitness
        fit = run_game_with_GA(pop[i])
        # add the fitness to the list with all the fitnesses
        fitness.append(fit)
    print("Largest Fitness:", np.max(fitness))
    print("Average Fitness:", np.mean(fitness))
    return np.array(fitness)

def select_mating_pool(pop, fitness, num_parents):
    # create an empty array for the parents depending on how many parents you want
    parents = np.empty((num_parents, pop.shape[1]))
    # iterate through all the parents
    for parent_num in range(num_parents):
        # find the best index for a parent given the fitnesses
        best_index = np.where(fitness == np.max(fitness))
        best_index = best_index[0][0]
        # slap it in the parents list
        parents[parent_num, :] = pop[best_index, :]
        fitness[best_index] = -99999999
    return parents

def crossover(parents, offspring_size):
    # create an empty offspring list
    offspring = np.empty(offspring_size)

    # For however many offspring you want (usually population size - parent size)
    for k in range(offspring_size[0]):
        # Continue until break
        (parent1_index, parent2_index) = (0, 0)
        while parent1_index == parent2_index:
            # randomly choose 2 parents
            parent1_index = random.randint(0, parents.shape[0] - 1)
            parent2_index = random.randint(0, parents.shape[0] - 1)
            # if both parents are different
            if parent1_index != parent2_index:
                # for every weight
                for j in range(offspring_size[1]):
                    # randomly choose a weight between the parents
                    if random.uniform(0, 1) < 0.5:
                        offspring[k, j] = parents[parent1_index, j]
                    else:
                        offspring[k, j] = parents[parent2_index, j]
            # if 2 parents are the same, keep on choosing
    return offspring

def mutation(offspring_crossover):
    # for every offspring
    for offspring_index in range(offspring_crossover.shape[0]):
        # iterate 25 times
        for _ in range(25):
            # in each iteration, randomly choose 25 weights
            i = random.randint(0, offspring_crossover.shape[1] - 1)

        # create a random value and modify the weights
        random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
        offspring_crossover[offspring_index, i] = offspring_crossover[offspring_index, i] + random_value
    return offspring_crossover
