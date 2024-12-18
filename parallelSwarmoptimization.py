from __future__ import division
import random
import math

#--- COST FUNCTION ------------------------------------------------------------+

# function we are attempting to optimize (minimize)
def func1(x):
    total = 0
    for i in range(len(x)):
        total += x[i]**2
    return total

#--- PARTICLE CLASS -----------------------------------------------------------+

class Particle:
    def __init__(self, x0, bounds):
        self.position_i = []          # particle position
        self.velocity_i = []          # particle velocity
        self.pos_best_i = []          # best position individual
        self.err_best_i = float('inf')  # best error individual
        self.err_i = float('inf')       # error individual

        for i in range(len(x0)):
            self.velocity_i.append(random.uniform(-1, 1))
            self.position_i.append(random.uniform(bounds[i][0], bounds[i][1]))

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.err_i = costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i:
            self.pos_best_i = self.position_i[:]
            self.err_best_i = self.err_i

    # update new particle velocity
    def update_velocity(self, pos_best_g, w=0.5, c1=1.5, c2=2.0):
        for i in range(len(self.position_i)):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, bounds):
        for i in range(len(self.position_i)):
            self.position_i[i] += self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            # adjust minimum position if necessary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]

#--- PSO CLASS ----------------------------------------------------------------+

class PSO:
    def __init__(self, costFunc, x0, bounds, num_particles, maxiter):
        self.num_dimensions = len(x0)
        self.err_best_g = float('inf')       # best error for group
        self.pos_best_g = []                 # best position for group
        self.swarm = [Particle(x0, bounds) for _ in range(num_particles)]
        self.costFunc = costFunc
        self.bounds = bounds
        self.num_particles = num_particles
        self.maxiter = maxiter

    def optimize(self):
        for i in range(self.maxiter):
            for particle in self.swarm:
                particle.evaluate(self.costFunc)

                # determine if current particle is the best (globally)
                if particle.err_i < self.err_best_g:
                    self.pos_best_g = particle.position_i[:]
                    self.err_best_g = particle.err_i

            for particle in self.swarm:
                particle.update_velocity(self.pos_best_g)
                particle.update_position(self.bounds)

            # Print iteration details
            print(f"Iteration {i+1}/{self.maxiter}, Best Fitness: {self.err_best_g}")

        # Print final results
        print('FINAL RESULTS:')
        print(f"Best Position: {self.pos_best_g}")
        print(f"Best Fitness: {self.err_best_g}")

#--- RUN ----------------------------------------------------------------------+

if __name__ == "__main__":
    initial = [5, 5]               # initial starting location [x1, x2, ...]
    bounds = [(-10, 10), (-10, 10)]  # input bounds [(x1_min, x1_max), (x2_min, x2_max), ...]
    num_particles = 15
    maxiter = 30

    print("Starting Particle Swarm Optimization...")
    optimizer = PSO(func1, initial, bounds, num_particles, maxiter)
    optimizer.optimize()
