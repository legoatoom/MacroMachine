
import os
import appdirs

__version__ = '0.0.1'
__name__ = 'macromachine'


'''
Current version of the program
'''

CONFIG_DIR = appdirs.user_config_dir(__name__)
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')
PIDFILE = f'/tmp/{__name__}.pid'
'''
Location of the PID file. It is tmp because we don't need it again after restart.
'''
