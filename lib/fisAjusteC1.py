import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from functools import reduce


# Generate universe variables
#   * inputs : ciclos y diversidad
#   C1  para PSO
def not_less_than_zero(v):
    return v if v >= 0 else 0.001

def fis_opt_Ajuste(ciclo, diversidad, grafica=False):

    x_ciclo = np.arange(0,11,.1)
    x_diversidad  = np.arange(0,15, .1)  ## el 11 es solo para graficar
    x_C1  = np.arange(-1.5, 3.5, .1)


    # Generate fuzzy membership functions trapezoidal y triangular
    ciclo_hi  = fuzz.trimf(x_ciclo, [6, 8, 10])
    ciclo_med = fuzz.trimf(x_ciclo, [3, 5, 7])
    ciclo_low = fuzz.trimf(x_ciclo, [0, 2, 4])

    diversidad_hi  = fuzz.trapmf(x_diversidad,  [4,6,15,20])
    diversidad_med = fuzz.trimf(x_diversidad,  [2.5,4,5.5])
    diversidad_low = fuzz.trimf(x_diversidad,  [0,2,3])

    C1_hi = fuzz.trimf(x_C1, [1, 2, 3])
    C1_med = fuzz.trimf(x_C1, [0, 1, 2])
    C1_low = fuzz.trimf(x_C1, [-1, 0, 1])

    # We need the activation of our fuzzy membership functions at these values.
    # This is what fuzz.interp_membership exists for!
    ciclo_level_hi = fuzz.interp_membership(x_ciclo, ciclo_hi, ciclo)
    ciclo_level_med = fuzz.interp_membership(x_ciclo, ciclo_med, ciclo)
    ciclo_level_low = fuzz.interp_membership(x_ciclo, ciclo_low, ciclo)

    diversidad_level_hi = fuzz.interp_membership(x_diversidad, diversidad_hi, diversidad)
    diversidad_level_med = fuzz.interp_membership(x_diversidad, diversidad_med, diversidad)
    diversidad_level_low = fuzz.interp_membership(x_diversidad, diversidad_low, diversidad)

    if grafica:
        # Visualize these universes and membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
        ax0.plot(x_ciclo, ciclo_hi, 'b', linewidth=1.5, label='High')
        ax0.plot(x_ciclo, ciclo_med, 'g', linewidth=1.5, label='Medium')
        ax0.plot(x_ciclo, ciclo_low, 'r', linewidth=1.5, label='Low')
        ax0.set_title('Cycles ')
        ax0.legend()

        ax1.plot(x_diversidad, diversidad_hi, 'b', linewidth=1.5, label='High')
        ax1.plot(x_diversidad, diversidad_med, 'g', linewidth=1.5, label='Medium')
        ax1.plot(x_diversidad, diversidad_low, 'r', linewidth=1.5, label='Low')
        ax1.set_title('Diversity')
        ax1.legend()

        ax2.plot(x_C1, C1_hi, 'b', linewidth=1.5, label='High')
        ax2.plot(x_C1, C1_med, 'g', linewidth=1.5, label='Medium')
        ax2.plot(x_C1, C1_low, 'r', linewidth=1.5, label='Low')
        ax2.set_title('C1')
        ax2.legend()


        # Turn off top/right axes
        for ax in (ax0, ax1, ax2):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()

    # Now we take our rules and apply them.
    # The OR operator means we take the maximum of these two.

    # Rule 1 si ciclo es hi y diversidad es hi entonces c1 es hi
    active_rule1 = np.fmin(ciclo_level_hi,diversidad_level_hi)
   # activation_1 = np.fmin(active_rule1, C1_hi)

    # Rule 2 si ciclo es hi y diversidad es med entonces c1 es hi
    active_rule2 = np.fmin(ciclo_level_hi, diversidad_level_med)
   # activation_2 = np.fmin(active_rule2, C1_hi)

    # Rule 3 si ciclo es hi y diversidad es low entonces c1 es hi
    active_rule3 = np.fmin(ciclo_level_hi, diversidad_level_low)
   # activation_3 = np.fmin(active_rule3, C1_hi)


    # Rule 4 si ciclo es med y diversidad es hi entonces c1 es med
    active_rule4 = np.fmin(ciclo_level_med, diversidad_level_hi)
    #activation_4 = np.fmin(active_rule4, C1_med)

    # Rule 5 si ciclo es med y diversidad es med entonces c1 es med
    active_rule5 = np.fmin(ciclo_level_med, diversidad_level_med)
    #activation_5 = np.fmin(active_rule5, C1_med)

    # Rule 6 si ciclo es med y diversidad es low entonces c1 es med
    active_rule6 = np.fmin(ciclo_level_med, diversidad_level_low)
    #activation_6 = np.fmin(active_rule6, C1_med)


    # Rule 7 si ciclo es low y diversidad es hi entonces c1 es low
    active_rule7 = np.fmin(ciclo_level_low, diversidad_level_hi)
    #activation_7 = np.fmin(active_rule7, C1_low)

    # Rule 8 si ciclo es low y diversidad es med entonces c1 es low
    active_rule8 = np.fmin(ciclo_level_low, diversidad_level_med)
    #activation_8 = np.fmin(active_rule8, C1_low)

    # Rule 9 si ciclo es low y diversidad es low entonces c1 es low
    active_rule9 = np.fmin(ciclo_level_low, diversidad_level_low)
    #activation_9 = np.fmin(active_rule9, C1_low)

    activation_rule_hi  = reduce(np.fmax, [active_rule1, active_rule2, active_rule3])
    activation_hi = np.fmin(activation_rule_hi, C1_hi)

    activation_rule_med = reduce(np.fmax, [active_rule4, active_rule5, active_rule6])
    activation_med = np.fmin(activation_rule_med, C1_med)

    activation_rule_low = reduce(np.fmax, [active_rule7, active_rule8, active_rule9])
    activation_low = np.fmin(activation_rule_low, C1_low)

    #aggregatedC1 = np.fmax(activation_9, (np.fmax(activation_8, np.fmax(activation_7,
     #               np.fmax(activation_6, np.fmax(activation_5, np.fmax(activation_4, np.fmax(activation_1,
      #              np.fmax(activation_2, activation_3)))))))))

    #aggregatedC1 = reduce(np.fmax,[activation_9,activation_8, activation_7,activation_6, activation_5, activation_4,
     #                             activation_3, activation_2,activation_1])

    aggregatedC1 = reduce(np.fmax, [activation_hi,activation_med,activation_low])

    # Calculate defuzzified result
    resultC1 = fuzz.defuzz(x_C1, aggregatedC1, 'centroid')
    activationC1 = fuzz.interp_membership(x_C1, aggregatedC1, resultC1)  # for plot

 #Visualize this
    if grafica:
        fig, ax0 = plt.subplots(figsize=(8, 3))

        ax0.fill_between(x_C1,  activation_hi, facecolor='b', alpha=0.7)
        ax0.plot(x_C1, C1_hi, 'b', linewidth=0.5, linestyle='--', )
        ax0.fill_between(x_C1, activation_med, facecolor='g', alpha=0.7)
        ax0.plot(x_C1, C1_med, 'g', linewidth=0.5, linestyle='--')
        ax0.fill_between(x_C1, activation_low, facecolor='r', alpha=0.7)
        ax0.plot(x_C1, C1_low, 'r', linewidth=0.5, linestyle='--')
        ax0.set_title('Output membership activity C1')

    if grafica:
        fig, ax0 = plt.subplots(figsize=(8, 3))
        ax0.plot(x_C1, C1_hi, 'b', linewidth=0.5, linestyle='--', )
        ax0.plot(x_C1, C1_med, 'g', linewidth=0.5, linestyle='--')
        ax0.plot(x_C1, C1_low, 'r', linewidth=0.5, linestyle='--')
        ax0.fill_between(x_C1,  aggregatedC1, facecolor='Orange', alpha=0.7)
        ax0.plot([resultC1, resultC1], [0, activationC1], 'k', linewidth=1.5, alpha=0.9)
        ax0.set_title('Aggregated membership and result (line) C1')

        plt.tight_layout()
        plt.show()
    return resultC1
if __name__ == '__main__':
    C1 = fis_opt_Ajuste(8, 1 ,True)

    print(C1)



 
