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

from copy import deepcopy
from controllers.benchmark import get_eval
import algorithms.algorithm_base as alg_base

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


def get_best_solutions(pop, k=3):
    pop = sorted(pop, key=lambda part: part.fitness.values)
    return deepcopy(pop[:k])



def main(config):
    size = config['list_size']
    total_evals = 0
    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=size, pmin=config['pmin'], pmax=config['pmax'], smin=config['smin'],
                     smax=config['smax'])
    toolbox.register("evaluate", get_eval(config['controller_module'],
                                          config['simulation']))  # parametro   get_eval(fis, px control)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    #toolbox.register("update", updateParticle, phi1=config['phi1'], phi2=config['phi2'])
    #pop = toolbox.population(n=config['pop_size'])
    alg_base.set_pop(config, toolbox, creator.Particle)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields
    
    pop = config['pop']
    GEN = config['ngen']
    best = None
    # Update fitness population
    for part in pop:
        total_evals += 1
        part.fitness.values = toolbox.evaluate(part)
        # print("fitness", part.fitness.values[0])
        # if not part.best or part.best.fitness < part.fitness:
        #    part.best = creator.Particle(part)
        #    part.best.fitness.values = part.fitness.values
        if not best or best.fitness < part.fitness:
            best = creator.Particle(part)
            best.fitness.values = part.fitness.values


    for g in range(GEN):
        g += 1
        # linearly decreased from 2 to 0
        a = 2 - 2 * g / (GEN - 1)
        list_best = list(map(np.array, get_best_solutions(pop, k=3)))


        pop_new = []
        for part in pop:
            A1, A2, A3 = a * (2 * np.random.uniform() - 1), a * (2 * np.random.uniform() - 1), a * (2 * np.random.uniform() - 1)
            C1, C2, C3 = 2 * np.random.uniform(), 2 * np.random.uniform(), 2 * np.random.uniform()
            X1 = list_best[0] - A1 * np.abs(C1 * list_best[0] - part)
            X2 = list_best[1] - A2 * np.abs(C2 * list_best[1] - part)
            X3 = list_best[2] - A3 * np.abs(C3 * list_best[2] - part)
            #print("new", pos_new)
            #print("part", part)

            pos_new = list((X1 + X2 + X3)/3)

            for i, x in enumerate(pos_new):
                if abs(x) < config['pmin']:
                    pos_new[i] = math.copysign(config['pmin'], x)
                elif abs(x) > config['pmax']:
                    pos_new[i] = math.copysign(config['pmax'], x)

            pop_new.append(creator.Particle(pos_new))

        # Update fitness population
        for part in pop_new:
            total_evals += 1
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
        logbook.record(gen=g, evals=total_evals, **stats.compile(pop))
        print(logbook.stream)
    #        config['Tiempo_Total'] = time.time() - inicio_tiempo

    #   return best.fitness, best, Tiempo_Total
    pop_regreso = alg_base.get_pop(pop)
    config = alg_base.save_config(config, time.time()-inicio_tiempo, 
                                  best.fitness.values[0], best, None, pop_regreso)
    return config


if __name__ == '__main__':
    config = {'pop_size': 20, 'ngen': 10, 'smin': -0.25, 'smax': 0.25,
              'pmin': 0, 'pmax': 1,
              'list_size': 10,  # numero de particulas
              'controller_module': 'fis5r10p',
              'simulation': 'rueda_trasera_fisopt',
              'runs': 1
              }
    print(main(config))
