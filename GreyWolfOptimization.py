import random
import math
import copy

# Fitness functions
def fitness_rastrigin(position):
    return sum(x**2 - 10 * math.cos(2 * math.pi * x) + 10 for x in position)

def fitness_sphere(position):
    return sum(x**2 for x in position)

# Wolf class
class Wolf:
    def __init__(self, fitness, dim, minx, maxx, seed):
        self.rnd = random.Random(seed)
        self.position = [self.rnd.uniform(minx, maxx) for _ in range(dim)]
        self.fitness = fitness(self.position)

def gwo(fitness, max_iter, n, dim, minx, maxx):
    rnd = random.Random(0)
    population = [Wolf(fitness, dim, minx, maxx, i) for i in range(n)]
    population.sort(key=lambda w: w.fitness)

    alpha_wolf, beta_wolf, gamma_wolf = copy.deepcopy(population[:3])

    for Iter in range(max_iter):
        if Iter % 10 == 0 and Iter > 0:
            print(f"Iter = {Iter} best fitness = {alpha_wolf.fitness:.3f}")

        a = 2 * (1 - Iter / max_iter)

        for wolf in population:
            A1, A2, A3 = [a * (2 * rnd.random() - 1) for _ in range(3)]
            C1, C2, C3 = [2 * rnd.random() for _ in range(3)]

            X1 = [alpha_wolf.position[j] - A1 * abs(C1 * alpha_wolf.position[j] - wolf.position[j]) for j in range(dim)]
            X2 = [beta_wolf.position[j] - A2 * abs(C2 * beta_wolf.position[j] - wolf.position[j]) for j in range(dim)]
            X3 = [gamma_wolf.position[j] - A3 * abs(C3 * gamma_wolf.position[j] - wolf.position[j]) for j in range(dim)]

            Xnew = [(X1[j] + X2[j] + X3[j]) / 3.0 for j in range(dim)]
            fnew = fitness(Xnew)

            if fnew < wolf.fitness:
                wolf.position = Xnew
                wolf.fitness = fnew

        population.sort(key=lambda w: w.fitness)
        alpha_wolf, beta_wolf, gamma_wolf = copy.deepcopy(population[:3])

    return alpha_wolf.position

# Driver code

def run_gwo(fitness, func_name, dim=3, num_particles=50, max_iter=100, minx=-10.0, maxx=10.0):
    print(f"\nBegin grey wolf optimization on {func_name} function\n")
    print(f"Goal is to minimize {func_name} in {dim} variables")
    print(f"Function has known min = 0.0 at ({', '.join(['0'] * dim)})")
    print(f"Setting num_particles = {num_particles}")
    print(f"Setting max_iter = {max_iter}\n")

    best_position = gwo(fitness, max_iter, num_particles, dim, minx, maxx)
    print(f"\nGWO completed\n")
    print(f"Best solution found: {[f'{x:.6f}' for x in best_position]}")
    print(f"Fitness of best solution = {fitness(best_position):.6f}\n")

# Run GWO for Rastrigin and Sphere functions
run_gwo(fitness_rastrigin, "Rastrigin")
