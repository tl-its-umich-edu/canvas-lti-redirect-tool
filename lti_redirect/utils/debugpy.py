from decouple import config
import debugpy

def config_to_bool(value): 
    return str(value).lower() in ('true', '1', 'yes', 'on')

def check_and_enable_debugpy():
    debugpy_enable = config_to_bool(config('DEBUGPY_ENABLE', default=False))
    debugpy_address =  '0.0.0.0'
    debugpy_port = 6020

    if debugpy_enable:
        print('DEBUGPY: Enabled Listening on ({0}:{1})'.format(debugpy_address, debugpy_port))
        debugpy.listen((debugpy_address, debugpy_port))