import importlib

def get_fis_controller(module):
    controller_name = 'controllers.{}'.format(module)
    mod = importlib.import_module(controller_name)
    return getattr(mod, 'fis_opt')

def get_simulation(simulation_module):
    simulation_name = 'simulations.{}'.format(simulation_module)
    simulation = importlib.import_module(simulation_name)
    return getattr(simulation, 'prueba_simulador')

def get_eval(fis_module, simulation_module):
    controller = get_fis_controller(fis_module)
    prueba_simulador = get_simulation(simulation_module)
    def eval(params):
        return prueba_simulador(params, controller)
    return eval

