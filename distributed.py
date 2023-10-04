# hacer al que inicia el experimento y ver como avanza y mezclando poblaciones
import random
from lib.diversity import diversidad  # importar los metodos para calcular la diversidad
from lib.fisAjusteC1_C2 import fis_opt_Ajuste  #llamar al fis para c1 y c2
#from lib.grafica_ajuste import metodo_grafica # llamar grafica
import redis
import json
import time
from popbuffer import PopBuffer
import os

#metodo para imprimir datos de configuracion de cada algoritmo
def Imprime_Config(poblaciones):

    for pob in poblaciones:
        #imprime toda la config
#       print(pob)
        #imprime en lista toda la info requerida
        print("\n {0}".format(pob["id"]))
       #print(pob["params"][pob["algorithm"]])
        for parametro in pob["params"][pob["algorithm"]]:
            print("{0}: {1:.4f}".format(parametro,pob[parametro]))


def Generador_de_poblaciones(strategies):
      # se van a ahacer 6 poblaciones iniciales
    poblaciones = []
    for i, algorithm in enumerate(strategies):
            configBasica = config.copy()
            configBasica['algorithm'] = algorithm
            configBasica['id'] = algorithm + "-" + str(i)
            for llave in configBasica:    #para sacar un valor aleatorio del rango
                if(type(configBasica[llave])==list and type(configBasica[llave][0])==float):
                    configBasica[llave]=random.uniform(configBasica[llave][0],configBasica[llave][1])
            poblaciones.append(configBasica)

    return poblaciones


def Setup(config):
    r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
    redis_ready = False
    # intenta hasta que este listo el contenedor
    while not redis_ready:
        try:
            redis_ready = r.ping()
        except:
            print("waiting for redis")
            time.sleep(3)

    # generar las poblaciones
    poblaciones=Generador_de_poblaciones(config["strategies"])

    # imprimir la lista de config llamar al metodo
    Imprime_Config(poblaciones)

    #enviamos las 5 poblaciones, lo vamos a hacer varias veces (for)
    for poblacion in poblaciones:
        mensaje = json.dumps(poblacion).encode('utf-8')
        r.lpush('cola_de_mensajes', mensaje)


def combina_buffer(config, random=False, uniqueBuffer=False):
    inicio_tiempo = time.time()
    popBuffer = PopBuffer(key=lambda x: x['score'], size=5)

    num_poblaciones_recibidas = 0
    num_total = 0
    total_evals = 0

    best_fitness = 5000
    best_solution = None

    while True:
        r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
        _, mensaje_poblacion = r.brpop('cola_evolucionada')

        if mensaje_poblacion:
            poblacion = json.loads(mensaje_poblacion)

            if 'dynamic_params' in config and config['dynamic_params'] == 'cycle':

                #print('Población recibida ... ')
                if 'num_cycle' not in poblacion:
                    poblacion['num_cycle'] = 1
                elif poblacion['num_cycle']<=9:
                    poblacion['num_cycle']+=1

            #if poblacion['algorithm'] == 'PSO':
                #poblacion['phi1'] = poblacion['phi1'] - poblacion['phi1'] * poblacion['num_pasada'] / config['num_cycles'] 
                #poblacion['phi2'] = poblacion['phi2'] - poblacion['phi2'] * poblacion['num_pasada'] / config['num_cycles'] 
                #print(poblacion['algorithm'], poblacion['id'],poblacion['phi1'])
                pop=[ind['solution'] for ind in poblacion['pop']]
                diver = diversidad(poblacion['best_solution'], pop)  # calcula la diverisdad
                print("ciclo={0}, diversidad={1}".format(poblacion['num_cycle'], diver))
                poblacion['phi1'], poblacion['phi2'] = fis_opt_Ajuste(poblacion['num_cycle'], diver, False)
                print("termina ciclo={0}, diversidad={1}, C1={2}, C2={3}".format(poblacion['num_cycle'], diver, poblacion['phi1'], poblacion['phi2']))
              #  metodo_grafica(poblacion['num_cycle'], diver, poblacion['phi1'], poblacion['phi2'])
            num_total += 1
            num_poblaciones_recibidas += 1
            total_evals += poblacion['total_num_eval']

            if poblacion["best_fitness"] < best_fitness:
                best_fitness = poblacion["best_fitness"]
                best_solution = poblacion["best_solution"]
            #imprimir los datos
            #print(poblacion['id'], poblacion['cxpb'], poblacion['mutpb'], poblacion['Best_fitness'],poblacion['Total_num_eval'])


            if num_total == config['num_poblaciones']*config['num_cycles']:   # para salirse cuando llegue a 10 poblacioens
                #print('ya son 12 poblaciones recibidas ...')
                total_time= time.time()-inicio_tiempo
                # imprime los resultados

                print("resultados del experimento")

                print(total_evals/total_time, total_time, total_evals)
                print("best score:{0} best solution {1}".format(best_fitness, best_solution))
                break

            print('pop:', poblacion['best_fitness'], poblacion['algorithm'], poblacion['id'], num_total)


            # esta es otra manera de migrar mas elitista
            poblacion['pop'].sort(key=lambda ind: ind['score'])
            #print(poblacion['pop'])

            # Save the best two populations to the buffer
            for ind in poblacion['pop'][:2]:
                if uniqueBuffer: 
                    if ind['score'] not in [ind['score'] for ind in popBuffer._list]:
                        popBuffer.append(ind)
                else:
                    popBuffer.append(ind)

            print('--------- original  ---------------------')
            for sol in poblacion['pop']:
                print(sol['score'])

            print('--------- buffer ---------------------')
            for sol in popBuffer._list:
                print(sol['score'])

            print('--------- modificada ---------------------')
            # replace the worst two individuals with two random from the buffer
            # poblacion['pop'] = poblacion['pop'][:-2] + [popBuffer.random_choice() for i in range(2)]
            if random:
                poblacion['pop'] = poblacion['pop'][:-2] + [popBuffer.random_choice() for i in range(2)]
            else:
                poblacion['pop'] = poblacion['pop'][:-2] + popBuffer.best(2)

            for sol in poblacion['pop']:
                print(sol['score'])
            print('------------------------------')



            # esta es una manera de migrar
            # mitad = len(mensajeA['pop'])//2  #sacas la long de la pop

            # mensajeA['pop'] = mensajeA['pop'][mitad:] + mensajeB['pop'][:mitad]
            # mensajeB['pop'] = mensajeB['pop'][mitad:] + mensajeA['pop'][:mitad]

            mensaje = json.dumps(poblacion).encode('utf-8')
            r.lpush('cola_de_mensajes', mensaje)




if __name__ == "__main__":
    config: None
    with open("config.json", "r") as conf_file:
        config = json.load(conf_file)
    Setup(config)
    combina_buffer(config, random=True, uniqueBuffer=True) # False Best, True Random
    # Cruce:
    # combina(config)


