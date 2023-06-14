file = open("bufTodo.txt")
results = {}
counter = 0
for line in file:
    if "diversidad" in line:
        columns = line.split()
        worker = columns[0]
        if worker not in results:
            results[worker] = []
        if "primero" in columns:
            results[worker].append({'diversidad':columns[4]})
        else:
            results[worker].append({'experiment':counter, 'gen': columns[2].split('=')[1],
                                    'diversidad':columns[3].split('=')[1],
                                    'c1': columns[4].split('=')[1], 'c2':columns[5].split('=')[1]})
        
    if "docker-compose" in line:
        counter+=1
        # print(columns)
for w in range(16):
    worker = 'worker_'+str(w+1)
    print(worker)
    for r in results[worker]:
        print(worker,r)
