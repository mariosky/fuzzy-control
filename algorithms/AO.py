# Example from:
# https://deap.readthedocs.io/en/master/examples/pso_basic.html#poli2007


import operator
import random

import numpy as np
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
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=0.5, smax=0.5, best=None)


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
    sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (
                1 / beta)
    u = np.random.normal(0, 1, dim) * sigma
    v = np.random.normal(1, dim)
    step = u / abs(v) ** (1 / beta)
    return step




def main(config):
    size = config['list_size']
    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=size, pmin=config['pmin'], pmax=config['pmax'], smin=config['smin'],
                     smax=config['smax'])
    toolbox.register("evaluate", get_eval(config['controller_module'],
                                          config['simulation']))  # parametro   get_eval(fis, px control)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    #toolbox.register("update", updateParticle, phi1=config['phi1'], phi2=config['phi2'])
    pop = toolbox.population(n=config['pop_size'])

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = config['ngen']
    best = None
    # Update fitness population
    for part in pop:
        part.fitness.values = toolbox.evaluate(part)
        # print("fitness", part.fitness.values[0])
        # if not part.best or part.best.fitness < part.fitness:
        #    part.best = creator.Particle(part)
        #    part.best.fitness.values = part.fitness.values
        if not best or best.fitness < part.fitness:
            best = creator.Particle(part)
            best.fitness.values = part.fitness.values


    for g in range(GEN):
        g += 1  # t starts at 1
        g1 = 2 * np.random.rand() - 1  # Eq. 16
        g2 = 2 * (1 - g / GEN)  # Eq. 17

        dim_list = np.array(list(range(1, size + 1)))
        miu = 0.00565
        r0 = 10
        r = r0 + miu * dim_list
        w = 0.005
        alpha = 0.1
        delta = 0.1
        phi0 = 3 * np.pi / 2
        phi = -w * dim_list + phi0
        QF = g ** ((2 * np.random.rand() - 1) / (1 - GEN) ** 2)  # Eq.(15)        Quality function
        x = r * np.sin(phi)  # Eq.(9)
        y = r * np.cos(phi)  # Eq.(10)



        x_mean = np.mean(np.array([np.array(part) for part in pop]), axis=0)  # Eq. 4
        #print("x_mean", x_mean)
        # Update positions
        pop_new = []
        for part in pop:
            if g <= (2 / 3) * GEN:  # Eq. 3

                if np.random.rand() < 0.5:
                    #print("Extended exploration")
                    pos_new = np.array(best) * (1 - (g + 1) / GEN) + \
                              np.random.rand() * (x_mean - np.array(best))
                else:
                    #print("Narrowed exploration")
                    random_part = random.choice(pop)
                    #print("random particle", random_part)
                    # Eq. 5:
                    pos_new = np.array(best) * get_simple_levy_step(size) + np.array(random_part) + np.random.rand() * (y - x)
            else:
                if np.random.rand() < 0.5:
                    #print("Extended exploitation")
                    pos_new = alpha * ( np.array(best) - x_mean) - np.random.rand() * \
                              (np.random.rand() * (config['pmax'] - config['pmin']) + config['pmin']) * delta  # Eq. 13
                else:
                    #print("Narrowed exploitation")
                    pos_new = QF * np.array(best) - (g2 * np.array(part) * np.random.rand()) - g2 * \
                              get_simple_levy_step(size) + np.random.rand() * g1  # Eq. 14.
            #print("new", pos_new)
            #print("part", part)

            for i, x in enumerate(pos_new):
                if abs(x) < config['pmin']:
                    pos_new[i] = math.copysign(config['pmin'], x)
                elif abs(x) > config['pmax']:
                    pos_new[i] = math.copysign(config['pmax'], x)

            pop_new.append(creator.Particle(pos_new))

        # Update fitness population
        for part in pop_new:
            part.fitness.values = toolbox.evaluate(part)
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values

        # Greedy Selection Pop
        pop = [pop_new[i] if pop_new[i].fitness.values < pop[i].fitness.values
                else pop[i] for i in range(len(pop))]

            #part[:] = list(map(operator.add, part, part.speed))

        # toolbox.update(part, best)

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


if __name__ == '__main__':
    config = {'pop_size': 50, 'ngen': 20, 'smin': -0.25, 'smax': 0.25,
              'pmin': 0, 'pmax': 1,
              'list_size': 10,  # numero de particulas
              'controller_module': 'fis5r10p',
              'simulation': 'rueda_trasera_fisopt',
              'runs': 1
              }
    print(main(config))