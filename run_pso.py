from algorithms import PSO
import csv
import json
import uuid

config = {'pop_size': 50,'ngen':20, 'smin':-0.25, 'smax':0.25,
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

with open("./results/{}-{}_config.json".format(config['controller_module'], experiment_id), "w") as outfile:
   json.dump(config, outfile)

for i in range(config['runs']):
   print("      run {}".format(i))
   result= PSO.main(config.copy())

   results.append((result['best_fitness'], result['best_solution'], result['tiempo_total'],result['total_num_eval']))
   
   with open('./results/temp_results.csv'.format(config['controller_module'], experiment_id),'a') as out:
      csv_out=csv.writer(out)
      csv_out.writerow(['best fitness','solution','time', 'evals'])
      for row in results:
          csv_out.writerow(row)

with open('./results/{}-{}_results.csv'.format(config['controller_module'], experiment_id),'w') as out:
   csv_out=csv.writer(out)
   csv_out.writerow(['best fitness','solution','time', 'evals'])
   for row in results:
       csv_out.writerow(row)
