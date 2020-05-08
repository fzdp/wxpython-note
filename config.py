import configparser
import os
import shutil

CONFIG = configparser.ConfigParser()

if not os.path.exists('config.ini'):
    shutil.copy('config.ini.example', 'config.ini')
CONFIG.read('config.ini')

if not os.path.exists(CONFIG['app']['data_dir']):
    os.mkdir(CONFIG['app']['data_dir'])

if not os.path.exists(CONFIG['app']['note_dir']):
    os.mkdir(CONFIG['app']['note_dir'])

if not os.path.exists(CONFIG['app']['index_dir']):
    os.mkdir(CONFIG['app']['index_dir'])
