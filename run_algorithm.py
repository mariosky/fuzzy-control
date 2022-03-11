#from algorithms import GWO
import csv
import json
import uuid
import importlib

def get_main(module):
    mod = importlib.import_module('algorithms.{}'.format(module))
    return getattr(mod, 'main')

config = { 'algorithm':'HS',
        'pop_size': 50,'ngen':20, 'smin':-0.25, 'smax':0.25,
        'pmin': 0, 'pmax': 1,
        'list_size':10,     #numero de particulas
        'controller_module':'fis5r10p',
        'simulation': 'rueda_trasera_fisopt',
        'runs':10
        }

main = get_main(config['algorithm'])

#print(PSO.main(config))

experiment_id= str(uuid.uuid4())[:8]
results = []

with open("./results/{}-{}_config.json".format(config['controller_module'], experiment_id), "w") as outfile:
   json.dump(config, outfile)

for i in range(config['runs']):
   print("      run {}-{}".format(i, config['algorithm']))
   result= main(config.copy())

   results.append((result['Best_fitness'], result['Best_Particle'], result['Tiempo_Total'],result['Total_num_eval']))
   
   with open('./results/{}-temp_results-{}-{}.csv'.format(config['algorithm'],config['controller_module'], experiment_id),'a') as out:
      csv_out=csv.writer(out)
      csv_out.writerow(['best fitness','particula','tiempo', 'evals'])
      for row in results:
          csv_out.writerow(row)

with open('./results/{}-{}_results.csv'.format(config['controller_module'], experiment_id),'w') as out:
   csv_out=csv.writer(out)
   csv_out.writerow(['best fitness','particula','tiempo', 'evals'])
   for row in results:
       csv_out.writerow(row)
