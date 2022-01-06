# Example from:
#https://deap.readthedocs.io/en/master/examples/pso_basic.html#poli2007


import operator
import random

import numpy
import math
from math import gamma
from deap import base
from deap import creator
import time
from deap import creator
from deap import tools

from controllers.benchmark import get_eval
# Minimizamos
# smin, smax velocidades máximas
#
inicio_tiempo = time.time()  # te asigna el tiempo actual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=0.5,smax=0.5, best=None)
# pmax y pmin rango de valores que va a tomar la partícula
# smin y smax velocidades máximas
def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
    part.speed = [random.uniform(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part

def get_simple_levy_step(dim):
        beta = 1.5
        sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        u = np.random.normal(0, 1, dim) * sigma
        v = np.random.normal(1, dim)
        step = u / abs(v) ** (1 / beta)
        return step

# phi1 y phi2 
# son los limites superiores del los valores aleatorios 
# de U_1 y U_2
# part.best la mejor posicion de la particula
# best, la mejor de todas.

def updateParticle(part, best, phi1, phi2):
    u1 = (random.uniform(0, phi1) for _ in range(len(part)))
    u2 = (random.uniform(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
    part[:] = list(map(operator.add, part, part.speed))

def main(config):
    size=config['list_size']
    toolbox = base.Toolbox()
    toolbox.register("particle", generate,  size=size, pmin=config['pmin'], pmax=config['pmax'], smin=config['smin'], smax=config['smax'])
    toolbox.register("evaluate", get_eval(config['controller_module'], config['simulation']))# parametro   get_eval(fis, px control)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", updateParticle, phi1=config['phi1'], phi2=config['phi2'])
    pop = toolbox.population(n=config['pop_size'])

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = config['ngen']
    best = None

    for g in range(GEN):
        g1 = 2 * np.random.rand() - 1  # Eq. 16
        g2 = 2 * (1 - epoch / g)  # Eq. 17

        dim_list = np.array(list(range(1, size + 1)))
        miu = 0.00565
        r0 = 10
        r = r0 + miu * dim_list
        w = 0.005
        phi0 = 3 * np.pi / 2
        phi = -w * dim_list + phi0
        x = r * np.sin(phi)  # Eq.(9)
        y = r * np.cos(phi)  # Eq.(10)
        
        #Update fitness population 
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values

        x_mean = np.mean(np.array( part.fitness for item in pop]), axis=0) # Eq. 4

        # Update positions
        for part in pop:
            
            if (g + 1) <= (2 / 3) * GEN  # Eq. 3
                if np.random.rand() < 0.5:
                    pos_new = best.speed * (1 - (g + 1) / GEN) + \
                              np.random.rand() * (x_mean - best.speed)
                else:
                    idx = np.random.choice(list(set(range(0, self.pop_size)) - {idx}))
                    pos_new = self.g_best[self.ID_POS] * self.get_simple_levy_step() + \
                              self.pop[idx][self.ID_POS] + np.random.rand() * (y - x)  # Eq. 5
            else:
                if np.random.rand() < 0.5:
                    pos_new = self.alpha * (self.g_best[self.ID_POS] - x_mean) - np.random.rand() * \
                              (nprandom.rand() * (self.problem.ub - self.problem.lb) + self.problem.lb) * self.delta  # Eq. 13
                else:
                    pos_new = QF * self.g_best[self.ID_POS] - (g2 * self.pop[idx][self.ID_POS] *
                            np.random.rand()) - g2 * self.get_simple_levy_step() + np.random.rand() * g1  # Eq. 14.

            u1 = (random.uniform(0, phi1) for _ in range(len(part)))
            u2 = (random.uniform(0, phi2) for _ in range(len(part)))
            v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
            v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
            part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
            for i, speed in enumerate(part.speed):
                if abs(speed) < part.smin:
                    part.speed[i] = math.copysign(part.smin, speed)
                elif abs(speed) > part.smax:
                    part.speed[i] = math.copysign(part.smax, speed)
            part[:] = list(map(operator.add, part, part.speed))

           #toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
#        config['Tiempo_Total'] = time.time() - inicio_tiempo
    
 #   return best.fitness, best, Tiempo_Total
    config['Tiempo_Total'] = time.time() - inicio_tiempo
    config['Total_num_eval'] = config['pop_size']
    config['Best_fitness'] = best.fitness.values[0]
    config['Best_Particle'] = best
    config['Estadistica_gen'] = stats.fields
    config['pop'] = pop
    return config
