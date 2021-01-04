import base64
import uuid
import random
import bcrypt
import datetime

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config = configparser.ConfigParser()


def get_base_url():
    """
    Return a base_url from the configuration
    
    :return:
    """
    try:
        base_url = config.get('econtextauth', 'base_url')
    except:
        base_url = ''
    return base_url


def generate_key():
    """
    Generate a key which is a unique combination of 25 random chars (0-9, A-Z)
    
    This key needs to be checked before it may be accepted by the mapper. Implementation of
    that depends on the mapper being selected.
    
    For example, with Neo4J
    >>> x = 0
    >>> while x < 100:
    >>>     api_id = generate_key()
    >>>     if not ApiKey.nodes.get_or_none(api_id, lazy=True):
    >>>         return api_id
    >>>     x += 1
    >>> raise Exception("Couldn't generate a unique apikey id in 100 tries. Please try again")
    
    :return:
    """
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for n in range(25))


def generate_uuid4():
    return str(uuid.uuid4())


def generate_secret() -> str:
    """
    Generate a secret

    :return:
    """
    return base64.b64encode(generate_uuid4().encode('utf8')).decode('utf8')


def hash_secret(secret) -> str:
    """
    Create a hash for a secret.
    
    This method can be used to hash an API Key secret, or also a user password.
    The secret can then be verified against the original:
    
    >>> unhashed_password = "some password goes here"
    >>> hashed_password = hash_secret(unhashed_password)
    >>> passed = bcrypt.checkpw(unhashed_password, hashed_password)

    :param secret: a string to hash
    :return: hashed secret
    """
    if isinstance(secret, (str,)):
        secret = secret.encode('utf8')
    return bcrypt.hashpw(secret, bcrypt.gensalt()).decode('utf8')


def compare_passwords(unhashed_password, hashed_password) -> bool:
    """
    Check a password and return True if it matches
    
    :param unhashed_password:
    :param hashed_password:
    :return:
    """
    if isinstance(unhashed_password, (str,)):
        unhashed_password = unhashed_password.encode('utf8')
    if isinstance(hashed_password, (str,)):
        hashed_password = hashed_password.encode('utf8')
    return bcrypt.checkpw(unhashed_password, hashed_password)


def parse_datetime(d) -> datetime.datetime:
    """
    Try to get a datetime from an input:
    
    * Try ISOFormat
    * From seconds since epoch
    
    :param d:
    :return:
    """
    o = None
    if isinstance(d, (datetime.datetime, )):
        o = d
    elif isinstance(d, (str,)):
        try:
            o = datetime.datetime.fromisoformat(d)
        except:
            pass
    elif isinstance(d, (int, float)):
        try:
            o = datetime.datetime.fromtimestamp(d)
        except:
            pass
    return o
