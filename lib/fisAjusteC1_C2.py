import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from functools import reduce

# Generate universe variables
#   * inputs : ciclos y diversidad
#   C1 y C2 para PSO
def not_less_than_zero(v):
    return v if v >= 0 else 0.001

def fis_opt_Ajuste(ciclo, diversidad, grafica):

    x_ciclo = np.arange(0, 11, .1)
    x_diversidad = np.arange(0, 20, .1)  ## el 11 es solo para graficar
    x_C1 = np.arange(1, 2, .1)
    x_C2 = np.arange(1, 2, .1)

    # Generate fuzzy membership functions trapezoidal y triangular
    ciclo_hi  = fuzz.trimf(x_ciclo, [7, 10, 13])
    ciclo_med = fuzz.trimf(x_ciclo, [2, 5, 8])
    ciclo_low = fuzz.trimf(x_ciclo, [-3, 0, 3])

    diversidad_hi  = fuzz.trapmf(x_diversidad,  [10,15,30,31])
    diversidad_med = fuzz.trimf(x_diversidad,  [5, 10 ,15])
    diversidad_low = fuzz.trimf(x_diversidad,  [-5,0,7])

    C1_hi = fuzz.trimf(x_C1, [1.5, 2, 2.5])
    C1_med = fuzz.trimf(x_C1, [1, 1.5, 2])
    C1_low = fuzz.trimf(x_C1, [0.5, 1, 1.5])

    C2_hi = fuzz.trimf(x_C2, [1.5, 2, 2.5])
    C2_med = fuzz.trimf(x_C2, [1, 1.5, 2])
    C2_low = fuzz.trimf(x_C2, [0.5, 1, 1.5])

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
        fig, (ax0, ax1, ax2,ax3) = plt.subplots(nrows=4, figsize=(8, 9))
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

        ax3.plot(x_C2, C2_hi, 'b', linewidth=1.5, label='High')
        ax3.plot(x_C2, C2_med, 'g', linewidth=1.5, label='Medium')
        ax3.plot(x_C2, C2_low, 'r', linewidth=1.5, label='Low')
        ax3.set_title('C2')
        ax3.legend()


        # Turn off top/right axes
        for ax in (ax0, ax1, ax2,ax3):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()

    # Now we take our rules and apply them.
    # The OR operator means we take the maximum of these two.

    # Rule 1 si ciclo es hi y diversidad es hi entonces c1 es hi y c2 es low
    active_rule1 = np.fmin(ciclo_level_hi,diversidad_level_hi)

    # Rule 2 si ciclo es hi y diversidad es med entonces c1 es hi y c2 es med
    active_rule2 = np.fmin(ciclo_level_hi, diversidad_level_med)

    # Rule 3 si ciclo es hi y diversidad es low entonces c1 es hi y c2 es low
    active_rule3 = np.fmin(ciclo_level_hi, diversidad_level_low)

    # Rule 4 si ciclo es med y diversidad es hi entonces c1 es med y c2 es hi
    active_rule4 = np.fmin(ciclo_level_med, diversidad_level_hi)

    # Rule 5 si ciclo es med y diversidad es med entonces c1 es med y c2 es med
    active_rule5 = np.fmin(ciclo_level_med, diversidad_level_med)

    # Rule 6 si ciclo es med y diversidad es low entonces c1 es med y c2 es low
    active_rule6 = np.fmin(ciclo_level_med, diversidad_level_low)

    # Rule 7 si ciclo es low y diversidad es hi entonces c1 es low y c2 es hi
    active_rule7 = np.fmin(ciclo_level_low, diversidad_level_hi)

    # Rule 8 si ciclo es low y diversidad es med entonces c1 es low y c2 es med
    active_rule8 = np.fmin(ciclo_level_low, diversidad_level_med)

    # Rule 9 si ciclo es low y diversidad es low entonces c1 es low y c2 es hi
    active_rule9 = np.fmin(ciclo_level_low, diversidad_level_low)

    activation_rule_hi_C1  = reduce(np.fmax, [active_rule1, active_rule2, active_rule3])
    activation_hi_C1 = np.fmin(activation_rule_hi_C1, C1_hi)

    activation_rule_med_C1 = reduce(np.fmax, [active_rule4, active_rule5, active_rule6])
    activation_med_C1 = np.fmin(activation_rule_med_C1, C1_med)

    activation_rule_low_C1 = reduce(np.fmax, [active_rule7, active_rule8, active_rule9])
    activation_low_C1 = np.fmin(activation_rule_low_C1, C1_low)

    aggregatedC1 = reduce(np.fmax, [activation_hi_C1,activation_med_C1,activation_low_C1])

    activation_rule_hi_C2 = reduce(np.fmax, [active_rule4, active_rule7, active_rule9])
    activation_hi_C2= np.fmin(activation_rule_hi_C2, C2_hi)

    activation_rule_med_C2 = reduce(np.fmax, [active_rule2, active_rule5, active_rule8])
    activation_med_C2 = np.fmin(activation_rule_med_C2, C2_med)

    activation_rule_low_C2 = reduce(np.fmax, [active_rule1, active_rule3, active_rule6])
    activation_low_C2 = np.fmin(activation_rule_low_C2, C2_low)

    aggregatedC2 = reduce(np.fmax, [activation_hi_C2, activation_med_C2, activation_low_C2])


    # Calculate defuzzified result
    resultC1 = fuzz.defuzz(x_C1, aggregatedC1, 'centroid')
    activationC1 = fuzz.interp_membership(x_C1, aggregatedC1, resultC1)  # for plot

    # Calculate defuzzified result
    resultC2 = fuzz.defuzz(x_C2, aggregatedC2, 'centroid')
    activationC2 = fuzz.interp_membership(x_C2, aggregatedC2, resultC2)  # for plot

 #Visualize this
    # if grafica:
    #     fig, ax0 = plt.subplots(figsize=(8, 3))
    #
    #     ax0.fill_between(x_C1,  activation_hi_C1, facecolor='b', alpha=0.7)
    #     ax0.plot(x_C1, C1_hi, 'b', linewidth=0.5, linestyle='--', )
    #     ax0.fill_between(x_C1, activation_med_C1, facecolor='g', alpha=0.7)
    #     ax0.plot(x_C1, C1_med, 'g', linewidth=0.5, linestyle='--')
    #     ax0.fill_between(x_C1, activation_low_C1, facecolor='r', alpha=0.7)
    #     ax0.plot(x_C1, C1_low, 'r', linewidth=0.5, linestyle='--')
    #     ax0.set_title('Output membership activity C1')
    #
    #     fig, ax1 = plt.subplots(figsize=(8, 3))
    #
    #     ax1.fill_between(x_C2, activation_hi_C2, facecolor='b', alpha=0.7)
    #     ax1.plot(x_C2, C2_hi, 'b', linewidth=0.5, linestyle='--', )
    #     ax1.fill_between(x_C2, activation_med_C2, facecolor='g', alpha=0.7)
    #     ax1.plot(x_C2, C2_med, 'g', linewidth=0.5, linestyle='--')
    #     ax1.fill_between(x_C2, activation_low_C2, facecolor='r', alpha=0.7)
    #     ax1.plot(x_C2, C2_low, 'r', linewidth=0.5, linestyle='--')
    #     ax1.set_title('Output membership activity C2')
    #
    # if grafica:
    #     fig, ax0 = plt.subplots(figsize=(8, 3))
    #     ax0.plot(x_C1, C1_hi,  'b', linewidth=0.5, linestyle='--')
    #     ax0.plot(x_C1, C1_med, 'g', linewidth=0.5, linestyle='--')
    #     ax0.plot(x_C1, C1_low, 'r', linewidth=0.5, linestyle='--')
    #     ax0.fill_between(x_C1,  aggregatedC1, facecolor='Orange', alpha=0.7)
    #     ax0.plot([resultC1, resultC1], [0, activationC1], 'k', linewidth=1.5, alpha=0.7)
    #     ax0.set_title('Aggregated membership and result (line) C1')
    #
    #     fig, ax1 = plt.subplots(figsize=(8, 3))
    #     ax1.plot(x_C2, C2_hi,  'b', linewidth=0.5, linestyle='--')
    #     ax1.plot(x_C2, C2_med, 'g', linewidth=0.5, linestyle='--')
    #     ax1.plot(x_C2, C2_low, 'r', linewidth=0.5, linestyle='--')
    #     ax1.fill_between(x_C2, aggregatedC2, facecolor='Orange', alpha=0.7)
    #     ax1.plot([resultC2, resultC2], [0, activationC2], 'k', linewidth=1.5, alpha=0.7)
    #     ax1.set_title('Aggregated membership and result (line) C2')
    #
    #     plt.tight_layout()
    #     plt.show()

    return resultC1,resultC2

if __name__ == '__main__':
    C1, C2 = fis_opt_Ajuste(10,4.602845965621419,True)
    print(C1,C2)
