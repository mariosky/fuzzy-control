import random

def save_config(config, tiempo_total, best_fitness, best_solution, stats, pop):
    config['tiempo_total'] = tiempo_total
    config['total_num_eval'] = config['pop_size']*config['ngen']
    config['best_fitness'] = best_fitness
    config['best_solution'] = best_solution
    config['stats'] = stats
    config['pop'] = pop
    return config


def set_pop(config, toolbox, creator_constructor):
    if 'pop' not in config:
        # si no esta la etiqueta en el diccionario se crea en el diccionario
        # en este caso se crea con objetos de DEAP
        config['pop'] = toolbox.population(n=config['pop_size'])
    else:
        pop = []  # crea una lista nueva
        for ind_dict in config['pop']:  # recorre la lista y lo pone en ind
            # es un constructor que crea individuos de deap que son compatibles

            nuevo = creator_constructor(ind_dict['solution'])
            nuevo.speed = [random.uniform(config['smin'], config['smax']) for _ in range(config['list_size'])]
            nuevo.smin = config['smin']
            nuevo.smax = config['smax']

            pop.append(nuevo)  # y los agrega a la lista
        config['pop'] = pop[:]  # renombra la poblacion para usar el mismo nombre mas adelante
    return config


def get_pop(pop):
    pop_regreso=[]
    for individuo in pop:
        # esto para que cada ind muestre su fitnes caundo lo imprima
        nuevo = {'solution': individuo, 'score': individuo.fitness.values[0]}
        pop_regreso.append(nuevo)
    return pop_regreso
