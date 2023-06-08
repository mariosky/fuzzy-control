import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def metodo_grafica(datos):
    arreglo=np.array(datos)
    # Visualizar las graficas
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3, figsize=(7, 9))
    ax0.set_xticks(arreglo[:, 0])
    ax0.plot(arreglo[:, 0], arreglo[:, 1], 'b*', label="diversidad")   #diversidad
    ax0.legend()
    ax0.set_xlabel("Generación")
    ax0.set_ylabel("Distancia")
    ax0.set_title("Gráfica para diversidad")
    ax1.set_xticks(arreglo[:, 0])
    ax1.plot(arreglo[:, 0], arreglo[:, 2], 'gs', label="C1")   #C1
    ax1.plot(arreglo[:, 0], arreglo[:, 3], 'ro', label="C2")     #c2
    ax1.legend()
    ax1.set_xlabel("Generación")
    ax1.set_ylabel("Coeficiente")
    ax1.set_title("Gráfica para C1 y C2")

    ax2.set_xticks(arreglo[:, 0])
    ax2.plot(arreglo[:, 0], arreglo[:, 4], 'kd', label="fitness")  # fitness
    ax2.legend()
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Fitness")
    ax2.set_title("Gráfica de Fitness")
    ax2.semilogy()

    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()


    plt.tight_layout()
    fig.savefig("C:/Users/Alejandra/fuzzy-control/plotParamPSO.png")
    plt.show()


if __name__ == '__main__':
    datos=[[1,3.5,6,2,6],
           [2,4.7,1,3,2],
           [3,2.2,2,9,1]]
    metodo_grafica(datos)



