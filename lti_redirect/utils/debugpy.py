from decouple import config
from distutils.util import strtobool
import debugpy


def forcebool(bool_str):
    if isinstance(bool_str, str):
        return strtobool(bool_str)
    return bool_str

def check_and_enable_debugpy():
    debugpy_enable = forcebool(config('DEBUGPY_ENABLE', default=False))
    debugpy_address =  '0.0.0.0'
    debugpy_port = 6020

    if debugpy_enable:
        print('DEBUGPY: Enabled Listening on ({0}:{1})'.format(debugpy_address, debugpy_port))
        debugpy.listen((debugpy_address, debugpy_port))