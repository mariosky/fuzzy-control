# Example from:
#https://deap.readthedocs.io/en/master/examples/pso_basic.html#poli2007

from lib.diversity import diversidad  # importar los metodos para calcular la diversidad
from lib.fisAjusteC1_C2 import fis_opt_Ajuste  #llamar al fis para c1 y c2
from lib.grafica_ajuste import metodo_grafica   #llamar al metodo para graficar
import operator
import random
import numpy
import math
import json
from deap import base
import time
from deap import creator
from deap import tools
from controllers.benchmark import get_eval
import algorithms.algorithm_base as alg_base

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
    # para variable c1 y c2
    toolbox.register("update", updateParticle, phi1=config['phi1'], phi2=config['phi2'])

    # pop = toolbox.population(n=config['pop_size'])
    alg_base.set_pop(config, toolbox, creator.Particle)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = config['ngen']
    pop = config['pop']
    best = None
    #imprime la diversinad inicial antes de evolucionar
    print("primero diversidad", diversidad(pop[0],pop))
  #imprime la poblacion creada
    print("poblacion",pop)
    #### datos=[]
    for g in range(GEN):
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values

        diver = diversidad(best, pop)
        ##phi1, phi2 = fis_opt_Ajuste(g+1, diver, False)
        ## para fijo c1 y c2
        if 'dynamic_parameters' in config:
            if config['none']:
                phi1 = config['phi1']
                phi2 = config['phi2']
        ##print("g={0}, diversidad={1}, C1={2}, C2={3}".format(g, diver, phi1, phi2))
            else:
                phi1, phi2 = fis_opt_Ajuste(g+1, diver, False)
        #### datos.append([g, diver, phi1, phi2,best.fitness.values[0]])

        for part in pop:
            #toolbox.update(part, best)
            updateParticle(part,best,phi1,phi2)
            # imprime la diversidd despues de acualizar en cada generacion
        #print("diversidad real", diversidad(best,pop))

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
#        config['Tiempo_Total'] = time.time() - inicio_tiempo
    #### metodo_grafica(datos)
    print(logbook.chapters)

    pop.pop(-1)
    pop.append(best)
    pop_regreso = alg_base.get_pop(pop)
    config = alg_base.save_config(config, time.time() - inicio_tiempo, best.fitness.values[0], best, None, pop_regreso)
    return config


if __name__ == "__main__":
    config = None
    with open(r"..\config.json", "r") as conf_file:
        config = json.load(conf_file)
    results = main(config)
    print(results)
