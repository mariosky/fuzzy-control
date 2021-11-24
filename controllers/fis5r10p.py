import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from  functools import reduce

# Generate universe variables
#   * inputs : error teta y error
#   obtener omega

def factor(valor, min, max):
    assert min < max
    return min+(max-min)*valor


def fis_opt(e_teta, error, params=[], grafica=False):
    a, b, c, d, e, f, g, h,i , j = list(map(abs,params))
    #print(params,e_teta, error)
    #factor_apertura = 1.3

    x_e_teta = np.arange(-100, 100, 0.5)
    x_error  = np.arange(-100, 100, 0.5)
    x_omega  = np.arange(-100, 100, 0.5)

    #x_e_teta = np.arange(-3, 3, 0.05)
    #x_error = np.arange(-3, 3, 0.05)
    #x_omega = np.arange(-3, 3, 0.05)

    # estas son las 5 funciones de membresia con parametros fijos

    # ver en variables modificada
    a = factor(a, 0,1) #(0,1)
    b = factor(b, 0.5, 2)    # (-2,-0.5)
    c = factor(c, 0, 2) # (0, 2)
    d = factor(d, 0.5, 1.5) # (.5 , 1.5)
    e = factor(e, 0, 1) # (0, 1)

    f =factor(f, 0, 1)  # (0,1)
    g = factor(g, 0.5, 2)  # (-2,0.5)
    h = factor(h, 0, 2) # (0, 2)
    i = factor(i, 0.5, 1.5) # (.5 , 1.5)
    j = factor(j, 0, 1)  # (0, 1)

    #print(a, b, c, d, e, f, g, h,i , j)
    # Generate fuzzy membership functions trapezoidal y triangular
    e_teta_hi_neg = fuzz.trapmf(x_e_teta, [-50, -5,-b, -b+c])
    e_teta_med_neg = fuzz.trimf(x_e_teta, [-d-e, -d, -d+e])
    e_teta_lo      = fuzz.trimf(x_e_teta, [-a, 0, a])
    e_teta_med_pos = fuzz.trimf(x_e_teta, [d-e, d, d+e])
    e_teta_hi_pos = fuzz.trapmf(x_e_teta, [b-c, b, 5, 50])

    error_hi_neg  = fuzz.trapmf(x_error, [-50, -5,-g, -g+h])
    error_med_neg = fuzz.trimf(x_e_teta, [-i-j, -i, -i+j])
    error_lo      = fuzz.trimf(x_error,  [-f, 0, f])
    error_med_pos = fuzz.trimf(x_e_teta, [i-j, i, i+j])
    error_hi_pos  = fuzz.trapmf(x_error, [g-h, g, 5, 50])

    omega_hi_neg  = fuzz.trapmf(x_omega,  [-50,-5,-1,-0.5])
    omega_med_neg = fuzz.trimf(x_omega,   [-1, -0.5, -0])
    omega_lo      = fuzz.trimf(x_omega,   [-0.5, 0, 0.5])
    omega_med_pos = fuzz.trimf(x_omega,   [0, 0.5, 1])
    omega_hi_pos  = fuzz.trapmf(x_omega,  [ 0.5, 1, 5, 50])

    # We need the activation of our fuzzy membership functions at these values.
    # This is what fuzz.interp_membership exists for!
    e_teta_level_hi_neg = fuzz.interp_membership(x_e_teta, e_teta_hi_neg, e_teta)
    e_teta_level_med_neg = fuzz.interp_membership(x_e_teta, e_teta_med_neg, e_teta)
    e_teta_level_lo = fuzz.interp_membership(x_e_teta, e_teta_lo, e_teta)
    e_teta_level_med_pos = fuzz.interp_membership(x_e_teta, e_teta_med_pos, e_teta)
    e_teta_level_hi_pos = fuzz.interp_membership(x_e_teta, e_teta_hi_pos, e_teta)

    error_level_hi_neg = fuzz.interp_membership(x_error, error_hi_neg, error)
    error_level_med_neg = fuzz.interp_membership(x_error, error_med_neg, error)
    error_level_lo = fuzz.interp_membership(x_error, error_lo, error)
    error_level_med_pos = fuzz.interp_membership(x_error, error_med_pos, error)
    error_level_hi_pos = fuzz.interp_membership(x_error, error_hi_pos, error)

    if grafica:
        # Visualize these universes and membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

        ax0.plot(x_e_teta, e_teta_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax0.plot(x_e_teta, e_teta_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax0.plot(x_e_teta, e_teta_lo, 'g', linewidth=1.5, label='Bajo')
        ax0.plot(x_e_teta, e_teta_med_pos, 'k', linewidth=1.5, label='Medio positivo')
        ax0.plot(x_e_teta, e_teta_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax0.set_title('Error Theta')
        ax0.legend()

        ax1.plot(x_error, error_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax1.plot(x_error, error_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax1.plot(x_error, error_lo, 'g', linewidth=1.5, label='Bajo')
        ax1.plot(x_error, error_med_pos, 'k', linewidth=1.5, label='Medio positivo')
        ax1.plot(x_error, error_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax1.set_title('Error')
        ax1.legend()

        ax2.plot(x_omega, omega_hi_neg, 'b', linewidth=1.5, label='Alto negativo')
        ax2.plot(x_omega, omega_med_neg, 'm', linewidth=1.5, label='Medio negativo')
        ax2.plot(x_omega, omega_lo, 'g', linewidth=1.5, label='Bajo')
        ax2.plot(x_omega, omega_med_pos, 'k', linewidth=1.5, label='Medio positivo')
        ax2.plot(x_omega, omega_hi_pos, 'r', linewidth=1.5, label='Alto positivo')
        ax2.set_title('Omega')
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
    # fmin regresa el minimo de los dos arreglos o valores
    # fmax regresa el maximo de los dos arreglos o valores
    # The OR operator means we take the maximum of these two.
    # The AND operator means we take el minimun of these two

    hi_neg_hi_neg =  np.fmin(e_teta_level_hi_neg, error_level_hi_neg)
    hi_neg_med_neg = np.fmin(e_teta_level_hi_neg, error_level_med_neg)
    hi_neg_lo =      np.fmin(e_teta_level_hi_neg, error_level_lo)
    hi_neg_med_pos = np.fmin(e_teta_level_hi_neg, error_level_med_pos)
    hi_neg_hi_pos =  np.fmin(e_teta_level_hi_neg, error_level_hi_pos)

    med_neg_hi_neg =  np.fmin(e_teta_level_med_neg, error_level_hi_neg)
    med_neg_med_neg = np.fmin(e_teta_level_med_neg, error_level_med_neg)
    med_neg_lo =      np.fmin(e_teta_level_med_neg, error_level_lo)
    med_neg_med_pos = np.fmin(e_teta_level_med_neg, error_level_med_pos)
    med_neg_hi_pos =  np.fmin(e_teta_level_med_neg, error_level_hi_pos)

    lo_hi_neg =  np.fmin(e_teta_level_lo, error_level_hi_neg)
    lo_med_neg = np.fmin(e_teta_level_lo, error_level_med_neg)
    lo_lo =      np.fmin(e_teta_level_lo, error_level_lo)
    lo_med_pos = np.fmin(e_teta_level_lo, error_level_med_pos)
    lo_hi_pos =  np.fmin(e_teta_level_lo, error_level_hi_pos)

    med_pos_hi_neg  = np.fmin(e_teta_level_med_pos, error_level_hi_neg)
    med_pos_med_neg = np.fmin(e_teta_level_med_pos, error_level_med_neg)
    med_pos_lo      = np.fmin(e_teta_level_med_pos, error_level_lo)
    med_pos_med_pos = np.fmin(e_teta_level_med_pos, error_level_med_pos)
    med_pos_hi_pos  = np.fmin(e_teta_level_med_pos, error_level_hi_pos)

    hi_pos_hi_neg  = np.fmin(e_teta_level_hi_pos, error_level_hi_neg)
    hi_pos_med_neg = np.fmin(e_teta_level_hi_pos, error_level_med_neg)
    hi_pos_lo      = np.fmin(e_teta_level_hi_pos, error_level_lo)
    hi_pos_med_pos = np.fmin(e_teta_level_hi_pos, error_level_med_pos)
    hi_pos_hi_pos  = np.fmin(e_teta_level_hi_pos, error_level_hi_pos)


    active_rule_hi_neg = reduce(np.fmax, [lo_hi_pos,
                                          hi_pos_lo,
                                          hi_pos_med_pos,
                                          hi_pos_hi_pos,
                                          ] )
    activation_hi_neg  = np.fmin(active_rule_hi_neg, omega_hi_neg)

    active_rule_med_neg = reduce(np.fmax,[
                                 med_pos_med_neg,
                                 med_pos_lo,
                                 med_pos_med_pos,
                                 med_pos_hi_pos,
                                 hi_pos_med_neg ])
    activation_med_neg = np.fmin(active_rule_med_neg, omega_med_neg)

    active_rule_lo = reduce(np.fmax,[
                                hi_neg_hi_pos,
                                med_neg_hi_pos,
                                lo_med_neg,
                                lo_lo,
                                lo_med_pos,
                                med_pos_hi_neg,
                                hi_pos_hi_neg])
    activation_lo = np.fmin(active_rule_lo, omega_lo)

    active_rule_med_pos = reduce(np.fmax, [
                                hi_neg_med_pos,
                                med_neg_hi_neg,
                                med_neg_med_neg,
                                med_neg_lo,
                                med_neg_med_pos])
    activation_med_pos = np.fmin(active_rule_med_pos, omega_med_pos)

    active_rule_hi_pos = reduce(np.fmax, [
                                hi_neg_hi_neg,
                                hi_neg_med_neg,
                                hi_neg_lo,
                                lo_hi_neg] )
    activation_hi_pos  = np.fmin(active_rule_hi_pos, omega_hi_pos)

    aggregated = reduce(np.fmax, [activation_hi_neg, activation_med_neg,activation_lo,activation_med_pos, activation_hi_pos ])
    # Calculate defuzzified result
    omega = fuzz.defuzz(x_omega, aggregated, 'centroid')
    #tip_activation = fuzz.interp_membership(x_omega, aggregated, omega)  # for plot


    return omega

if __name__ == '__main__':
    # = fis_opt(-1.0225139922075002, -1.5029882118831652,[0.9054750552355649, 1.313749939916838, 1.2115608804558582, 1.0984015671585659,0.9054750552355649, 1.313749939916838, 1.2115608804558582, 1.0984015671585659],True)
    #omega = fis_opt(-1.0225139922075002, -1.5029882118831652,
                    #[.5,1,1,1,.5,1,1,1]
     #               [0.904678677722167, 0.8175345617149045, 0.13224560900960503, 0.5469457556076623, 0.5325770579589316,
      #               0.9268987320027717, 0.9800203897134122, 0.24073473149479774]
       #              , True)
    #omega= fis_opt(1.0572916680894755 ,-0.92007166,[0.19590043465383156, 0.7167493393335032, 0.9350616308752682, 0.2737485279962393, 0.9197640201658847, 0.9344545773709528, 0.2746576593220633, 0.662691565472217],True)
    #omega = fis_opt( -0.8579203417523265, -2.02587306, [0.6158061060468809, 0.4832258519402056, 0.7864552296026883, 0.5862045721640615, 0.6798355710879616, 0.386040327866486, 0.6634239215587792, 0.38294084619747026], True)
    #print(omega) ## debe imprimir -1.5385706528567843e-17
    omega = fis_opt(-1.053091629254558,4.5266952810876880,
                    [0.8959158028155084, 0.658995053052556, 0.676739138745285, 0.559788140918265, 1.0342303561818451,
                     -0.06451794622238155, 0.4669683430430709, 0.6595549547377009, 0.5788390726539321,
                     1.1403916447411557]
                    ,True)

