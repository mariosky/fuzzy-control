from algorithms import GA
import csv
import json
import uuid

config = {'pop_size': 50, 'ngen':20, 'cxpb':0.7, 'mutpb':0.3,
        'list_size': 9,  # numero de genes en el cromosoma
        'controller_module':'fis3f9p',
        'simulation':'rueda_trasera_fisopt',
        'runs':30,
        'ini_min':0, 'ini_max':1
        }


experiment_id= str(uuid.uuid4())[:8]
results = []
for i in range(config['runs']):
    print("      run {}".format(i))
    result = GA.main(config.copy()) 
    results.append((result['Best_fitness'], result['Tiempo_Total'], result['Total_num_eval'], result['Best_solution']))




with open("./results/{}-{}_config.json".format(config['controller_module'], experiment_id), "w") as outfile:
    json.dump(config, outfile)

with open('./results/{}-{}_results.csv'.format(config['controller_module'], experiment_id),'w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Best','Time','Evals', 'Best_solution' ])
    for row in results:
        csv_out.writerow(row)
