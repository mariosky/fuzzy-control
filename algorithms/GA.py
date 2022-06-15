import random
import time
import json  # formato de texto universal
from controllers.benchmark import get_eval
from deap import base
from deap import creator
from deap import tools
import algorithms.algorithm_base as alg_base

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)


def main(config):
    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("attr_float", random.uniform, config['ini_min'],config['ini_max'])

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, config['list_size']) # parametro
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", get_eval(config['controller_module'], config['simulation']))# parametro
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma= 0.2, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    #empezar a contar el tiempo
    inicio_tiempo = time.time()  # te asigna el tiempo actual
    #random.seed(64)
    best = None

    alg_base.set_pop(config, toolbox, creator.Individual)
    pop = config['pop']

          #Calcular fitness
    fitnesses = map(toolbox.evaluate, pop) # se evalua toda la poblacion

    tot_num_ev= len(pop)
    #Asignar fitness a cada individuo

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    #crear una lista para guardar los fitness de todas las generaciones
    #lista_fitness=[]
    #lista_gen=[]
    #lista_eval=[]
    # se hace mejor un una lista para guardar todos los datos anteriores
    estadistica_gen=[]

    for gen in range(config['ngen']):
        # decendencia
        print("gen:",gen)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        #cruce
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability cxpb
            if random.random() < config['cxpb']:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
        #mutacion
        for mutant in offspring:
            # mutate an individual with probability mutpb
            if random.random() < config['mutpb']:
                toolbox.mutate(mutant)
                # hacer los valores positivos
                del mutant.fitness.values


        #actualiza poblacion, son los ind que se les borro el fitness porque muto

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # copia  la nueva
        pop[:] = offspring

        #imprime estadistica
        num_ev_gen = len(invalid_ind)
        tot_num_ev = tot_num_ev + num_ev_gen
         #  ordenar los fitness
        fits = [ind.fitness.values[0] for ind in pop]

        estadistica_gen.append([num_ev_gen,min(fits)])

    #crear un diccionario para cambiar los individuos deap a formato
    pop_regreso = alg_base.get_pop(pop)

    config = alg_base.save_config(config, time.time() - inicio_tiempo, min(fits), tools.selBest(pop, 1)[0], estadistica_gen, pop_regreso)
    # config['tiempo_total']=time.time()-inicio_tiempo
    # config['total_num_eval'] = tot_num_ev
    # config['best_fitness'] = min(fits)
    # config['best_solution'] = tools.selBest(config['pop'], 1)
    # config['estadistica_gen'] = estadistica_gen

    #ya que saco las estadisticas anteriores cambia la poblacion
    # config['pop'] = pop_regreso
    return config


if __name__ == "__main__":
    config = None
    with open(r"..\config.json", "r") as conf_file:
        config = json.load(conf_file)
    results = main(config)
    print(results)

