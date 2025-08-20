from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from simulations.ruta_curvas import CubicSplinePath, Pi_2_pi
import math
import warnings

from importlib import import_module

L= 2.9  # longitud del vehiculo en mts
KTH = 1.0   # constante de ajuste k2
KE = 0.3    # constanste k
Kp = 1

ERROR_MAX = 10 # En metros

# hacer el modelo matematico de la moto que es lo que se va a controlar
def modelo(z, t, delta, aceleracion):
    x, y, teta, v = z
    dx_dt    = v * np.cos(teta)
    dy_dt    = v * np.sin(teta)
    dteta_dt = v / L * np.tan(delta)
    dv_dt    = aceleracion

    return [dx_dt, dy_dt,dteta_dt,dv_dt]

# este metodo lo reemplazaremos con el FIS para que nos regrese delta
def control_rueda_trasera(v, yaw0, e, k, yaw_ref, params, controller):
    #calcular el error
    error_teta = Pi_2_pi(yaw0 - yaw_ref)
    omega = 0.0 
    if not controller:
        omega = v * k * math.cos(error_teta) / (1.0-k*e) - KTH * abs(v) * error_teta- KE * v * math.sin(error_teta) / error_teta * e
    else:
        omega = controller(error_teta, e, params=params)
        
    if error_teta == 0.0 or omega == 0.0 or v == 0.0:
        return 0.0

    delta = math.atan2(L * omega / v, 1.0)
    return delta


def calc_target_speed(yaw, yaw_ref, direction):
    target_speed = 10 / 3

    dyaw = yaw_ref - yaw
    switch = math.pi / 4.0 <= dyaw < math.pi / 2.0

    if switch:
        direction *= -1
        return 0.0, direction

    if direction != 1:
        return -target_speed, direction

    return target_speed, direction

def pid_control(velocidad_objetivo, v):
    a = Kp * (velocidad_objetivo - v)
    return a


# definir el estado inicial
def simulacion(ruta, meta_objetivo, params, controller):
    # posiciones iniciales
    x0 = 0.0
    y0 = 0.0
    yaw0 = 0.0
    v0 = 0.0
    s0 = 0

    x=[x0]
    y=[y0]
    yaw=[yaw0]
    error_teta = []
    v=[v0]
    direction =1
    z0 = x0, y0, yaw0, v0
    error=[]

    # defines un arreglo de los tiempos que vas a medir de 0-10 seg, y los partes en 100 pedazos
    # lo pones en 101 para que haga 100 pedazos
    t = np.linspace(1, 50,501)
    
    di=0
    aceleracion = 0


    for i in range(len(t)-1):

        goal_flag=False
        error_flag=False

        # di = metodo de control
        # aceleracion
        # control_rueda_trasera = feedback por la retroaliemntacion que da
        e, k, yaw_ref, s0 = ruta.calc_track_error(x0, y0, s0)
        # estaba en 100, vamos a ver que pasa si lo reducimos a 10
        if abs(e)>ERROR_MAX:
            #pass
            error_flag = True
            break

        error.append(e)
        error_t = Pi_2_pi(yaw0 - yaw_ref)
        error_teta.append(error_t)

        try:
            di = control_rueda_trasera(v0, yaw0, e, k, yaw_ref,params, controller)
        except Exception as ex:
            #print(ex, controller, params)
            error_flag = True
            break

        speed_ref, direction = calc_target_speed(yaw0, yaw_ref, direction)
        aceleracion = pid_control(speed_ref, v0)

        inputs = (di, aceleracion)

        z = None
        # correr el modelo
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z=odeint(modelo, z0, [0,0.1], args=inputs)

        z0 = z[-1]
        x0, y0, yaw0, v0 = z0  #le asignas el ultimo valor de z que es donde estan los valores

        x.append(x0)
        y.append(y0)
        yaw.append(yaw0)
        v.append(v0)

        dx = x0 - meta_objetivo[0]
        dy = y0 - meta_objetivo[1]

        if math.hypot(dx,dy) <= 0.3:
               #print("META")
            goal_flag = True
            break

    sim_trace = {
        'i':i, # tiempo
        'x':x,
        'y':y,
        'yaw':yaw,
        'v':v,
        'error':error,
        'error_flag':error_flag,
        'goal_flag':goal_flag,
        'error_teta':error_teta,
        'v':v
        }

    return sim_trace

def rmse_error(sim_trace):
    error=sim_trace['error']
    error_rmse = math.sqrt(sum([e ** 2 for e in error]) / len(error))
    #error_rmse = sum([e ** 2 for e in error]) / len(error) ** .5
    #print('error:',error, ', error_rmse:', error_rmse, 'len(error)',  len(error))
    return error_rmse

def rmse_teta_error(sim_trace):
    error=sim_trace['error_teta']
    error_teta = math.sqrt(sum([e ** 2 for e in error]) / len(error))
    return error_teta

def composite(sim_trace):
    print(sim_trace['error'])
    print(sim_trace['error_teta'])
    errors = [min(e, ERROR_MAX) for e in sim_trace['error']]
    error_norm = math.sqrt(sum([(e/ERROR_MAX)**2 for  e in  errors])/len(errors))
    teta_norm =  math.sqrt(sum([(et/math.pi)**2 for et in sim_trace['error_teta']])/len(sim_trace['error_teta']))
    return error_norm + teta_norm

def prueba_simulador(params, controller, grafica=False,calc_metrica=composite ):
    # puntos para definir la ruta m
    #ax = [0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0]
    #ay = [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]
    # puntos para definir la ruta A
    #ax = [0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0]
    #ay = [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]
    # puntos para definir la ruta s
    #ax = [0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0]
    #ay = [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]

    #lista_rutas=[[[0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]]]
    #lista_rutas= [[[0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0],[0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]]]
    #lista_rutas = [[[0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0],[0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]]]

    # tres rutas juntas - rutas M A S
    lista_rutas=[[[0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0,  5.0, 6.5, 3.0, 5.0, -2.0]],
      [[0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0], [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]],
      [[0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0],[0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]]]

    #rutas nueva 1-2-3
    #lista_rutas = [[[0.0, -2.5, 5.0, 7.5], [0.0, -4.0, 6.0,  6.5]],
    #               [[0.0,  2.5, 5.0, 8.0], [0.0,  4.0, 6.0, -6.5]],
    #               [[0.0, 1.0, -6.0, 1.0, 5.0, 6.5], [0.0, -5.0, 1.0, 3.0, -2.0, -4.5]]]

    # rutas nueva 4-5-6
    #lista_rutas = [[[0.0, 2.0, -4.0, 6.0, 6.5], [0.0, 3.5,  -2.0, -3.0,-1.5]],
     #             [[0.0, 2.0, -3.0, -1.5,3.0, 7.5], [0.0, 3.5, -2.0, -4.5,-3.0,-1.5]],
      #             [[0.0, 1.0, -6.0, 1.0, 5.0, 6.5], [0.0, -5.0, 1.0, 3.0, -2.0, -4.5]]]

    suma_error=0
    for ax, ay in lista_rutas:

        error_ruta =  rutas(ax, ay, params, controller,  grafica, calc_metrica=composite)
        print(error_ruta)

        suma_error += error_ruta[0]

    fit_ruta = suma_error/float(len(lista_rutas))
    #print(fit_ruta)
    return fit_ruta,



def rutas(ax, ay, params,controller, grafica=False, calc_metrica=composite):  # metodo a llamar 3 veces
        ruta_referencia = CubicSplinePath(ax,ay)
        meta_objetivo = [ax[-1], ay[-1]]
        sim_trace = simulacion(ruta_referencia, meta_objetivo, params, controller)


        #assert goal_flag
        #spline = np.arange(0, ruta_referencia.length, 0.1)
        #t = np.linspace(0, 50, 501)
        #t= t[:i+2]
        #yaw_pi = map(Pi_2_pi,yaw)
        if sim_trace['error_flag']:
            #print("Bad Controller")
            return 5000,
        if not sim_trace['goal_flag']:
            #print("no llego")
            return 2000,
        #error_rmse = sum([i**2 for i in error])/len(error)**.5
        # print(error_rmse)
        # return error_rmse,

        #plt.plot(ax,ay, "xb", label="Input")
        #plt.plot(-1,1, "*b",label = "punto")
        #valor_s=ruta_referencia.__find_nearest_point(.1, -1, 1)
        #grafica=True

        if grafica:
            i = sim_trace['i']
            x = sim_trace['x']
            y = sim_trace['y']
            yaw = sim_trace['yaw']
            v = sim_trace['v']

            spline = np.arange(0, ruta_referencia.length+0.09, 0.1)
            t = np.linspace(0, 50, 501)
            t= t[:i+2]
            yaw_pi = map(Pi_2_pi,yaw)

            plt.subplots(1)
            plt.plot(ax, ay, "xb", label="spline")
            plt.plot(ruta_referencia.X(spline),ruta_referencia.Y(spline), "-r", label= "route")
            plt.plot(x, y, "-g", label= "tracking")
            plt.axis("equal")
            plt.grid(True)
            plt.xlabel("x (mts)")
            plt.ylabel("y (mts)")
            plt.legend()


            plt.subplots(1)
            plt.plot(t, np.rad2deg(list(yaw_pi)), "-r", label="yaw")
            plt.grid(True)
            plt.xlabel("time (seg)")
            plt.ylabel("theta (degrees)")
            plt.legend()

            plt.subplots(1)
            plt.plot(spline, np.rad2deg(ruta_referencia.calc_yaw(spline)),"-r", label="yaw-reference")
            plt.grid(True)
            plt.xlabel("line length (mts)")
            plt.ylabel("yaw angle (degrees)")
            plt.legend()

            plt.subplots(1)
            plt.plot(t, v, "-b", label="velocity")
            plt.grid(True)
            plt.xlabel("time (seg)")
            plt.ylabel("velocity (m/s)")
            plt.legend()

            plt.show()
        #print(error)
        # error_rmse = sum([i ** 2 for i in error]) / len(error) ** .5
        #print("error score",error_rmse)

        return calc_metrica(sim_trace),

if __name__ == '__main__':
    # controlador 3 funciones memb con 9 param
    #from controllers.fis3f9p import fis_opt
    #controller = fis_opt
    #prueba_simulador([0.5100006103689083, -0.41621313195522447, 0.8251985475495492, 0.4114258655863874, 0.495287507338406, 0.24805299883193144, 1.6146050014785913, 0.1643118499073945, 0.22840629626085052],controller, True)

    # controlador 5 funciones memb con 10 param

    from controllers.fis5r10p import fis_opt
    controller = fis_opt
    #solution = [0.7895321425599207, 0.486514381925796, 0.43022274249683146, 0.6975676982390971, 0.8879391004878989, 0.9609521360233566, -0.13154647245644002, 0.367185601048029, 0.6047960207170928, 0.7793810182327733]
   # GA dist random
    #solution = [0.7768964906544156, 0.46909805836507723, 0.5103526342066431, 0.13044685606216389, 0.7240377193482798,
     # 0.7482000242171565, -0.11848494169586468, 0.3693990345164646, 0.5130603848064309, 0.26815382954624345]
   # pso dist random
    solution = [1.2608916932647793, 0.7547613509797118, 0.668591039970935, 0.7152843678740539, 0.41160203689842134, 0.7977923532384195, 0.17806985980006212, 0.4116991499925696, 0.9031368976692209, 0.38472799969726906]
    #solution= [0.8709967026625609, 0.49392685125942104, 0.49345240075548097, 0.8851056525795413, 0.33678843917887763,
    #           0.5504857686029268, 0.19623961717228944, 0.427810851387937, 0.14215853775480675, 0.8012346657671614]
    #pso-ga dist random
   # solution=[0.7228889765417605, 0.40351333467758754, 0.4088168945555207, 0.9433884354410893, 0.4087422359415779,
    # 0.43795220847539307, 0.1725155830272853, 0.407057101686224, 0.23996038582469367, 0.4341681231562077]

    #from controllers.fis5r15p import fis_opt

    #controller = fis_opt
# pso dist rand 16 wk
    #solution=[0.8866388283444326, 1.2461094606337797, 0.9723771623602855, 0.26054912040203726, 0.8218162139572471,
    # 0.5426226437795528, 0.12187459704529674, 0.3512880959062574, 0.7756751569520165, 0.9576507430043677,
    # 0.11823549309021017, 1.246493524412821, 0.33841318179410396, 0.7336983941620179, 0.8281641987075132]
# GWO dis rand 16 wk
    #solution = [0.7258097008145802, 0.6981852052542457, 0.6178064167865922, 0.8954640724296591, 0.9666233623719824,
     #       0.34947795907873963, 0.1895713902477333, 0.41148826219192913, 0.9656961450523518, 0.9519132784816658,
      #      0.7665525238600003, 0.5252830484994827, 0.4238565670123952, 0.9661658743721423, 0.300021302728231]

    # PSO-GWO dis rand 16 wk
    #solution = [0.8414225696123507, 0.27592532310914947, 0.2603595486747314, 0.31171055122530844, -0.27865674777318167,
    solution = [0.7429843188865688, 0.4426409707487153, 0.5198999727835202, 0.8149645785722207, 0.9810647390895578, 0.5124523418132632, 0.44131889063161944, 0.6339344377860096, 0.46356873484114935, 0.3558191816820483]
    solution = [0.8711494989571718, 0.5368013051342952, 0.47210631897614264, 0.48682313713082537, 0.7201401519559807, 0.6879296831673701, 0.4198061456392319, 0.6114770094224073, -0.2266788274123966, 0.4856464315119331]
    solution = [0.6066034327346437, 0.6603566530460818, 0.8912308315947914, 0.014873224963206602, 0.8045841275499558,
     0.6916140152090308, -0.08729050245281324, 0.390533904852554, 0.48972674653273507, -0.27200095431963367]
    # 0.6768718211400274, -0.0016381118010724467, 0.2697389189824962, 0.5791988038875634, 0.3672806044221338,
    # 0.5655157430878895, 0.557365716911244, 0.8282824765261503, 0.019522309904360036, 0.6243469278786694]
    res = prueba_simulador(solution,controller, True, calc_metrica=composite)
    print(res)
