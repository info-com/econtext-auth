#from econtextauth.models import application, group, user

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config = configparser.ConfigParser()


def get_base_url():
    try:
        base_url = config.get('econtextauth', 'base_url')
    except:
        base_url = ''
    return base_url