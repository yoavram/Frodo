import os.path
import inspect
import ConfigParser

def working_folder():
    #return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.dirname(__file__)

def configuration():
    folder = working_folder()
    filepath = folder + os.path.sep + 'frodo.properties'
    cfg = ConfigParser.ConfigParser()
    cfg.read(filepath)
    return cfg

def hosts():
    folder = working_folder()
    filepath = folder + os.path.sep + 'hosts'
    return filepath

if __name__ == '__main__':
    pass
