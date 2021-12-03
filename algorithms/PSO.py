# Example from:
#https://deap.readthedocs.io/en/master/examples/pso_basic.html#poli2007


import operator
import random

import numpy
import math

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
    toolbox = base.Toolbox()
    toolbox.register("particle", generate,  size=config['list_size'], pmin=config['pmin'], pmax=config['pmax'], smin=config['smin'], smax=config['smax'])
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
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)

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
