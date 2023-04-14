from math import sqrt

def distancia_euclidiana(punto1,punto2):
    distancia=sqrt(sum([(a-b)**2 for a,b in zip(punto1,punto2)]))
    return distancia

def diversidad(best,pop):
    return sum([distancia_euclidiana(best,soluc) for soluc in pop])

if __name__ == '__main__':
    best=[0.39011121631048107, 0.28163671651108224]
    pop=[[0.39011121631048107, 0.28163671651108224],[0.6847453826163694, 0.41952512043399315],[0.38890729661766127,0.41952512043399315],[3,1]]
    print(diversidad(best,pop))

