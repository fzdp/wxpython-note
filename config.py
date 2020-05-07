import configparser
import os

CONFIG = configparser.ConfigParser()

if os.path.exists('config.ini'):
    CONFIG.read('config.ini')
else:
    CONFIG['app'] = {}
    CONFIG['app']['data_dir'] = 'data'
    CONFIG['app']['note_dir'] = 'notes'

    CONFIG['database'] = {}
    CONFIG['database']['db_file'] = os.path.join(CONFIG['app']['data_dir'], 'note.sqlite')

    with open('config.ini', 'w') as file:
        CONFIG.write(file)

if not os.path.exists(CONFIG['app']['data_dir']):
    os.mkdir(CONFIG['app']['data_dir'])

if not os.path.exists(CONFIG['app']['note_dir']):
    os.mkdir(CONFIG['app']['note_dir'])
