import random
import numpy as np

# Fitness function
def fitness(chromosome):
    x = int(''.join(map(str, chromosome)), 2)
    return x ** 2

# Generate a random chromosome
def generate_chromosome(length):
    return [random.randint(0, 1) for _ in range(length)]

# Generate an initial population
def generate_population(size, chromosome_length):
    return [generate_chromosome(chromosome_length) for _ in range(size)]

# Select two parents based on their fitness
def select_pair(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    parent1 = population[random.choices(range(len(population)), weights=selection_probs)[0]]
    parent2 = population[random.choices(range(len(population)), weights=selection_probs)[0]]
    return parent1, parent2

# Crossover between two parents
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2

# Mutate a chromosome
def mutate(chromosome, mutation_rate):
    return [gene if random.random() > mutation_rate else 1 - gene for gene in chromosome]

# Parameters
population_size = 10
chromosome_length = 5
mutation_rate = 0.01
generations = 20

# Initialize population
population = generate_population(population_size, chromosome_length)

for generation in range(generations):
    # Calculate fitness for each chromosome
    fitnesses = [fitness(chromosome) for chromosome in population]
    print(f"Generation {generation + 1} best fitness: {max(fitnesses)}")

    # Create a new generation
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = select_pair(population, fitnesses)
        offspring1, offspring2 = crossover(parent1, parent2)
        offspring1 = mutate(offspring1, mutation_rate)
        offspring2 = mutate(offspring2, mutation_rate)
        new_population.extend([offspring1, offspring2])

    # Replace the old population
    population = new_population
