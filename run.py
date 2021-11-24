from algorithms import GA
import csv
import json
import uuid

config = {'pop_size': 10,'cxpb':0.7, 'mutpb':0.3, 'ngen':2,
        'controller_module':'fis5r10p',
        'simulation':'rueda_trasera_fisopt',
        'runs':2
        }


experiment_id= str(uuid.uuid4())[:8]
results = []
for i in range(config['runs']):
    print("      run {}".format(i))
    result = GA.main(config.copy()) 
    results.append((result['Best_fitness'][0], result['Tiempo_Total'], result['Total_num_eval'], result['Best_solution']))
    result = GA.main(config.copy()) 



with open("{}-{}_config.json".format(config['controller_module'], experiment_id), "w") as outfile:
    json.dump(config, outfile)

with open('{}-{}_results.csv'.format(config['controller_module'], experiment_id),'w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Best','Time','Evals', 'Best_solution' ])
    for row in results:
        csv_out.writerow(row)
