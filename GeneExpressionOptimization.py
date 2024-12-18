# Optimization via gene expression
import random

# Fitness function: minimize f(x) = x^2
def fitness(x):
    return -x**2  # Negative because higher fitness is better

# Generate initial population
def generate_population(size, lower, upper):
    return [random.uniform(lower, upper) for _ in range(size)]

# Crossover
def crossover(parent1, parent2):
    alpha = random.random()
    return alpha * parent1 + (1 - alpha) * parent2

# Mutation
def mutate(gene, mutation_rate, lower, upper):
    if random.random() < mutation_rate:
        return random.uniform(lower, upper)
    return gene

# Main Genetic Algorithm
def genetic_algorithm(pop_size, generations, mutation_rate, lower, upper):
    population = generate_population(pop_size, lower, upper)
    for _ in range(generations):
        # Evaluate fitness
        population.sort(key=fitness, reverse=True)
        new_population = []

        # Selection and reproduction
        for i in range(pop_size // 2):
            parent1, parent2 = random.choices(population[:pop_size // 2], k=2)
            child = mutate(crossover(parent1, parent2), mutation_rate, lower, upper)
            new_population.extend([parent1, child])

        population = new_population

    # Best solution
    best_gene = max(population, key=fitness)
    return best_gene, -fitness(best_gene)

# Run the algorithm
best_solution, best_fitness = genetic_algorithm(50, 100, 0.1, -10, 10)
print(f"Best Solution: {best_solution}, Fitness: {best_fitness}")
