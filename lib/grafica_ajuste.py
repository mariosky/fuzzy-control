import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def metodo_grafica(datos):
    arreglo=np.array(datos)
    # Visualizar las graficas
    # fig, (ax0, ax1,ax2) = plt.subplots(nrows=3, figsize=(7, 9))
    # ax0.plot(arreglo[:, 0], arreglo[:, 1], 'b*', label="diversidad")   #diversidad
    # ax0.legend()
    # ax0.set_xlabel("Generación")
    # ax0.set_ylabel("distancia")
    # ax0.set_title("Gráfica para diversidad")
    #
    # ax1.plot(arreglo[:, 0], arreglo[:, 2], 'gs', label="C1")   #C1
    # ax1.plot(arreglo[:, 0], arreglo[:, 3], 'ro', label="C2")     #c2
    # ax1.legend()
    # ax1.set_xlabel("Generación")
    # ax1.set_ylabel("coeficiente")
    # ax1.set_title("Gráfica para C1 y C2")
    # for ax in (ax0, ax1, ax2, ax3):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()

    fig, (ax0, ax2) = plt.subplots(nrows=2, figsize=(7, 9))
    ax0.set_title("Gráfica Diversidad y C1 y C2")
    color="tab:red"
    ax0.set_xticks(arreglo[:,0])
    ax0.yaxis.set_major_locator(MultipleLocator(1.0))
    ax0.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax0.set_xlabel("Generación")
    ax0.set_ylabel("Distancia",color=color)
    a1=ax0.plot(arreglo[:, 0], arreglo[:, 1], '-d', label="Diversidad",color=color)   #diversidad
    print("valor Diversidad",arreglo[:, 1])
    ax0.tick_params(axis="y", labelcolor=color)

    ax1=ax0.twinx()

    color = "tab:green"
    ax1.set_ylabel("Coeficientes C1 y C2",color=color)
    a2=ax1.plot(arreglo[:, 0], arreglo[:, 2], '-s', label="C1",color=color)   #C1
    a3=ax1.plot(arreglo[:, 0], arreglo[:, 3], '-o', label="C2",color="orange")     #c2
    ax1.tick_params(axis="y", labelcolor=color)

# para juntar las etquetas de todos los ejes legend
#     ax=a1+a2+a3
#     labs=[l.get_label() for l in ax]
#     ax0.legend(ax,labs,loc=0)
    # tambien se puede usar de esta manera
   # fig.legend(loc=0)
    # o tambien de esta manera
    ax0.legend(handles=a1+a2+a3)

    ax2.set_xticks(arreglo[:, 0])
    ax2.plot(arreglo[:, 0], arreglo[:, 4], 'kd', label="fitness")  # fitness
    ax2.legend()
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Fitness")
    ax2.set_title("Gráfica de Fitness")
    ax2.semilogy()
    #ax2.ylim(0,10**-5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.get_xaxis().tick_bottom()
    ax2.get_yaxis().tick_left()


    plt.tight_layout()
    fig.savefig("C:/Users/Alejandra/fuzzy-control/plotParamPSO.png")
    plt.show()


if __name__ == '__main__':
    datos=[[1,3.5,6,2,6],
           [2,4.7,1,3,2],
           [3,2.2,2,9,1]]
    metodo_grafica(datos)



