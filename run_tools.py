import importlib


def get_main(module):
    mod = importlib.import_module('algorithms.{}'.format(module))
    return getattr(mod, 'main')