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

# Minimizamos
# smin, smax velocidades máximas
#
inicio_tiempo = time.time()  # te asigna el tiempo actual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=0.5, smax=0.5, best=None)


def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size))
    part.speed = [random.uniform(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part





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
    n_new = 50
    c_r = 0.95
    pa_r = 0.05
    fw = 0.0001 * (config["pmax"] - config["pmin"])
    fw_damp = 0.9995
    dyn_fw = fw

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

        # Update positions
        pop_new = []
        for part in pop:
            pos_new = creator.Particle(random.uniform(config['pmin'], config['pmax']) for _ in range(size))

            for j in range(size):
                # Use Harmony Memory
                if np.random.uniform() <= c_r:
                    pos_new[j] = random.choice(pop)[j]
                # Pitch Adjustment
                if np.random.uniform() <= pa_r:
                    delta = dyn_fw * np.random.normal(config['pmin'], config['pmax'])  # Gaussian(Normal)
                    pos_new[j] += delta

            for i, x in enumerate(pos_new):
                if abs(x) < config['pmin']:
                    pos_new[i] = math.copysign(config['pmin'], x)
                elif abs(x) > config['pmax']:
                    pos_new[i] = math.copysign(config['pmax'], x)

            pop_new.append(pos_new)

        # Update Damp Fret Width
        dyn_fw *= fw_damp

        # Update fitness population
        for part in pop_new:
            total_evals += 1
            part.fitness.values = toolbox.evaluate(part)
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values

        # Merge Harmony Memory and New Harmonies, Then sort them, Then truncate extra harmonies
        pop = sorted(pop+pop_new, key=lambda part: part.fitness.values)
        pop = deepcopy(pop[:config['pop_size']])

        # toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
    #        config['Tiempo_Total'] = time.time() - inicio_tiempo

    #   return best.fitness, best, Tiempo_Total
    config['Tiempo_Total'] = time.time() - inicio_tiempo
    config['Total_num_eval'] = total_evals
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