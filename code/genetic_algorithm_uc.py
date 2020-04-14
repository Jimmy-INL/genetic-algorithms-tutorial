#!/usr/bin/env python3

from math import ceil
import copy
import random

def genetic_algorithm(el_p, to_p, dim, epochs, function):
	population = initialize_population(POP_SIZE, dim, SEARCH_MIN, SEARCH_MAX)
	for e in range(1, epochs+1):
		population = sorted(population, key=function)
		mating_pool = []
		elites = elite_selection(population, el_p)
		del population[:len(elites)]
		t_winner = tournament_selection(population, to_p)
		mating_pool.extend(elites)
		mating_pool.append(t_winner)
		population = evolve(mating_pool, elites)
		mating_pool.clear()
	population = sorted(population, key=function)
	best_fitness = function(population[0])
	print(f'Best minimum found was {best_fitness:.2f}.')

def evolve(mating_pool, elites):
	new_population = []
	new_population.extend(elites)
	while len(new_population) < POP_SIZE:
		p_a_idx = random.randrange(len(mating_pool))
		p_b_idx = random.randrange(len(mating_pool))
		if p_a_idx == p_b_idx:
			continue
		parent_a = mating_pool[p_a_idx]
		parent_b = mating_pool[p_b_idx]
		child_a, child_b = crossover(parent_a, parent_b)
		child_a = mutation(child_a, SEARCH_MIN, SEARCH_MAX)
		child_b = mutation(child_b, SEARCH_MIN, SEARCH_MAX)
		new_population.append(child_a)
		new_population.append(child_b)
	return new_population

def crossover(parent_a, parent_b):
	if random.uniform(0.00, 1.00) >= CROSS_RATE:
		return copy.deepcopy([parent_a, parent_b])
	child_a, child_b = [], []
	pivot = random.randint(1, len(parent_a)-1)
	for i in range(0, len(parent_a)):
		if i < pivot:
			child_a.append(parent_a[i])
			child_b.append(parent_b[i])
		else:
			child_a.append(parent_b[i])
			child_b.append(parent_a[i])
	return child_a, child_b
	
def mutation(child, s_min, s_max):
	for i in range(len(child)):
		if random.uniform(0.00, 1.00) <= MUTAT_RATE:
			diff = random.uniform(s_min*0.5, s_max*0.5)
			child[i] += diff
			child[i] = max(child[i], s_min)
			child[i] = min(child[i], s_max)
	return child

def elite_selection(population, percent):
	elites = []
	for i in range(ceil(len(population)*percent)):
		elites.append(population[i])
	return elites

def tournament_selection(population, percent):
	tournament = []
	for i in range(ceil(len(population)*percent)):
		random_idx = random.randint(0, len(population)-1)
		tournament.append(population.pop(random_idx))
	tournament = sorted(tournament, key=styb_tang)
	return tournament[0]

def styb_tang(point):
	summ = 0
	for d in point:
		summ += d**4 - (16 * d**2) + (5 * d)
	return (1 / 2) * summ

def initialize_population(size, dim, min, max):
	population = []
	for _ in range(size):
		point = []
		for _ in range(dim):
			point.append(random.uniform(min, max))
		population.append(point)
	return population

if __name__ == '__main__':
	SEARCH_MIN, SEARCH_MAX = -5.00, 5.00
	DIMENSIONS = 2
	POP_SIZE = 200
	ELITE_PROPORTION = 0.01
	TOURN_PROPORTION = 0.02
	EPOCHS = 10
	CROSS_RATE, MUTAT_RATE = 0.95, 0.05
	genetic_algorithm(ELITE_PROPORTION, TOURN_PROPORTION, DIMENSIONS, \
		EPOCHS, styb_tang)