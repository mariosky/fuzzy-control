from algorithms import PSO
import csv
import json
import uuid

config = {'pop_size': 10,'ngen':3, 'smin':-0.5, 'smax':0.5,
        'pmin': 0, 'pmax': 1,
        'list_size':10,     #numero de particulas
        'controller_module':'fis5r10p',
        'simulation': 'rueda_trasera_fisopt',
        'runs':1,
        'phi1': 2.0, 'phi2': 2.0
        }

#print(PSO.main(config))

experiment_id= str(uuid.uuid4())[:8]
results = []
for i in range(config['runs']):
   print("      run {}".format(i))
   result= PSO.main(config.copy())

   results.append((result['Best_fitness'], result['Best_Particle'], result['Tiempo_Total'],result['Total_num_eval']))


with open("./results/{}-{}_config.json".format(config['controller_module'], experiment_id), "w") as outfile:
   json.dump(config, outfile)

with open('./results/{}-{}_results.csv'.format(config['controller_module'], experiment_id),'w') as out:
   csv_out=csv.writer(out)
   csv_out.writerow(['best fitness','particula','tiempo', 'evals'])
   for row in results:
       csv_out.writerow(row)
