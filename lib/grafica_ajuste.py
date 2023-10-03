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
    ax0.set_title("Diversity Plot for C1 and C2")
    color="tab:red"
    ax0.set_xticks(arreglo[:,0])
    ax0.yaxis.set_major_locator(MultipleLocator(1.0))
    ax0.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax0.set_xlabel("Cycles")
    ax0.set_ylabel("Distance",color=color)
    a1=ax0.plot(arreglo[:, 0], arreglo[:, 1], '-d', label="Diversity",color=color)   #diversidad
    print("valor Diversidad",arreglo[:, 1])
    ax0.tick_params(axis="y", labelcolor=color)

    ax1=ax0.twinx()

    color = "tab:green"
    ax1.set_ylabel(" C1 and C2 Coefficients",color=color)
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
    ax2.set_xlabel("Cycles")
    ax2.set_ylabel("Fitness")
    ax2.set_title("Fitness Plot")
    ax2.semilogy()
    #ax2.ylim(0,10**-5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.get_xaxis().tick_bottom()
    ax2.get_yaxis().tick_left()


    plt.tight_layout()
    fig.savefig("C:/Users/Alejandra/fuzzy-control/plotParamPSO.pdf")
    plt.show()


if __name__ == '__main__':
          # ciclo, diversidad, c1,c2,fitness
    datos=[[1, 15.03,  0,    2,    0.07],
           [2, 11.05,  0.02, 1.25, 0.07],
           [3, 11,     0.03, 1.27, 0.05],
           [4, 10.39,  0.85, 1.14, 0.05],
           [5, 8.7,    1,    1,    0.05],
           [6, 6.5,    1.35, 0.75, 0.05],
           [7, 7.8,    1.40, 1.07, 0.035],
           [8, 7.3,    1.68, 1.05, 0.035],
           [9, 7.2,    1.79, 1.08, 0.035],
           [10, 7.0,   2,    1.05, 0.035],

           ]
    metodo_grafica(datos)



