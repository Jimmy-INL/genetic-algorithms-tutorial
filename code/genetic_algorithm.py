#!/usr/bin/env python3

from math import ceil
import copy
import random

def genetic_algorithm(el_p, to_p, dim, epochs, function):
	"""Genetic algorithm driver.
	Initializes the population and evolves it over time.

	Parameters:
		el_p : the proportion of elites for elite selection.
		to_p : the proportion of tournament entrants for tournament selection.
		dim : dimensionality of the problem.
		epochs : how many iterations of the evolution algorithm to perform.
		function : the fitness function to evolve from.
	"""
	# initially the population is random
	population = initialize_population(POP_SIZE, dim, SEARCH_MIN, SEARCH_MAX)
	for e in range(1, epochs+1): # for each iteration
		population = sorted(population, key=function) # sort by fitness
		mating_pool = [] # init empty mating pool
		# select elites based on best fitness in population
		elites = elite_selection(population, el_p)
		# delete elites from population
		del population[:len(elites)]
		# select tournament winner from random candidates
		t_winner = tournament_selection(population, to_p)
		# add the elites to the mating pool
		mating_pool.extend(elites)
		# add the tournament winner to the mating pool
		mating_pool.append(t_winner)
		# evole the population based on parents and genetic operators
		population = evolve(mating_pool, elites)
		mating_pool.clear() # erase the mating pool for next generation
	# sort population by fitness again
	population = sorted(population, key=function)
	best_fitness = function(population[0])
	print(f'Best minimum found was {best_fitness:.2f}.')

def evolve(mating_pool, elites):
	"""Evolves population based on genetic operators.

	Parameters:
		mating_pool : where to select parents from.
		elites : previously found elites.

	Returns:
		A new population of offspring from mating pool.
	"""
	new_population = [] # store new population as list
	new_population.extend(elites) # add elites verbatim
	while len(new_population) < POP_SIZE: # while population isn't at max size
		# get both parents indices
		p_a_idx = random.randrange(len(mating_pool))
		p_b_idx = random.randrange(len(mating_pool))
		# we don't mind parents have identical genes but we don't
		# want the parents to use the same index. Parent A can be
		# equal to Parent B, but Parent A cannot be Parent B
		if p_a_idx == p_b_idx:
			continue
		# get the parents from indices
		parent_a = mating_pool[p_a_idx]
		parent_b = mating_pool[p_b_idx]
		# find children using crossover
		child_a, child_b = crossover(parent_a, parent_b)
		# mutate each child
		child_a = mutation(child_a, SEARCH_MIN, SEARCH_MAX)
		child_b = mutation(child_b, SEARCH_MIN, SEARCH_MAX)
		# add children to population
		new_population.append(child_a)
		new_population.append(child_b)
	return new_population

def crossover(parent_a, parent_b):
	"""One-point crossover operator.

	Parameters:
		parent_a : the first parent.
		parent_b : the second parent.

	Returns:
		Two child chromosomes as a product of both parents.
	"""
	# only perform crossover based on the crossover rate
	if random.uniform(0.00, 1.00) >= CROSS_RATE:
		return copy.deepcopy([parent_a, parent_b])
	child_a, child_b = [], []
	# find a pivot point at random
	pivot = random.randint(1, len(parent_a)-1)
	for i in range(0, len(parent_a)):
		# before pivot, use genes from one parent
		if i < pivot:
			child_a.append(parent_a[i])
			child_b.append(parent_b[i])
		# after pivot, use genes from second parent
		else:
			child_a.append(parent_b[i])
			child_b.append(parent_a[i])
	return child_a, child_b
	
def mutation(child, s_min, s_max):
	"""Mutation operator.

	Parameters:
		child : the chromosome to mutate.
		s_min : the lower bound for mutation.
		s_max : the upper bound for mutation.

	Returns:
		A mutated child.
	"""
	for i in range(len(child)):
		# only perform mutation based on the mutation rate
		if random.uniform(0.00, 1.00) <= MUTAT_RATE:
			# find a random distance within 50% radius
			diff = random.uniform(s_min*0.5, s_max*0.5)
			# update the child axes with that distance
			child[i] += diff
			# the position is now randomized but still relatively close
			# if it's outside the search space, clamp it to within
			child[i] = max(child[i], s_min)
			child[i] = min(child[i], s_max)
	return child

def elite_selection(population, percent):
	"""Elite selection function.
	Stores elites to bring into the next generation and mating pool.

	Parameters:
		population : the population to take elites from.
		percent : the proportion of the population to consider elites.

	Returns:
		A list of elite solutions.
	"""
	elites = []
	# grab percent% best individuals
	for i in range(ceil(len(population)*percent)):
		elites.append(population[i]) # and append to elites
	return elites

def tournament_selection(population, percent):
	"""Tournament selection function.
	Creates a tournament of random individuals and returns the best.

	Parameters:
		population : the population to take tournament from.
		percent : the proportion of the population who enters the tournament.

	Returns:
		Best fit individual from tournament.
	"""
	tournament = []
	# grab percent% random individuals
	for i in range(ceil(len(population)*percent)):
		random_idx = random.randint(0, len(population)-1)
		tournament.append(population.pop(random_idx)) # append to tournament
	tournament = sorted(tournament, key=styb_tang) # sort by fitness
	return tournament[0] # return best fit from tournament

def styb_tang(point):
	"""GA fitness function.
	Uses Styblinski-Tang Function in d dimensions.

	Parameters:
		point : a point in d-space.

	Returns:
		The fitness of that point.
	"""
	summ = 0
	for d in point:
		summ += d**4 - (16 * d**2) + (5 * d)
	return (1 / 2) * summ

def initialize_population(size, dim, min, max):
	"""Initializes a random population.

	Parameters:
		size : the size of the population.
		dim : the dimensionality of the problem
		min : the minimum in a dimension for the search space.
		max : a maximum in a dimension for the search space.

	Returns:
		A random population of that many points within the bounds of the space.
	"""
	population = [] # population stored as a list
	for _ in range(size): # for the size of the population
		point = [] # point as well as a list
		for _ in range(dim): # to fill each axes
			# generate a random position for that axes
			point.append(random.uniform(min, max))
		population.append(point) # add to population
	return population

if __name__ == '__main__':
	# bounds for the search space
	SEARCH_MIN, SEARCH_MAX = -5.00, 5.00
	DIMENSIONS = 2 # dimensionality of the problem
	POP_SIZE = 200 # how big is the population
	ELITE_PROPORTION = 0.01 # proportion of elites
	TOURN_PROPORTION = 0.02 # proportion of tournament
	EPOCHS = 10 # how many generations to run for
	# generatic operator chances
	CROSS_RATE, MUTAT_RATE = 0.95, 0.05
	genetic_algorithm(ELITE_PROPORTION, TOURN_PROPORTION, DIMENSIONS, \
		EPOCHS, styb_tang)