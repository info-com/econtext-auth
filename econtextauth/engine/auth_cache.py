"""
Provide an in-memory store so that we don't need to go to the database
for every login attempt. This solves a problem when we have hundreds or
thousands of calls to the Auth API with the same credentials. It can
also be used to prevent someone from using the same IP address to try
multiple username and password combinations, although that requires
that we start making a note of the incoming IP address.
"""
from datetime import datetime


class AuthCache(object):
    
    def __init__(self, size=50, ip_attempt_limit=20, *args, **kwargs):
        """
        :param size int: The number of attempts to remember
        """
        self.size = size
        self.ip_attempt_limit = ip_attempt_limit
        self.ip_index = dict()
        self.auth_index = dict()
        pass
    
    def check_auth(self, auth):
        """
        Check whether an authentication attempt has occurred.
        
        This should also write a timestamp somewhere so that we know when
        when this check occurred. We only get rid of attempts that haven't
        occurred recently.
        
        * check whether this specific username+password has been used already
        * check whether repeated attempts from the same IP have been used
        
        THe auth parameter looks like this:
        
            {
                "type": "username" | "apikey",
                "credential": {
                    "username": "USERNAME",
                    "password": "PASSWORD"
                },
                "application": "APPLICATION"
            }
        
        :return bool False when we detect "abuse"
        """
        
        if self.check_credentials(auth):
            "If we detect too many attempts with the same credentials..."
            return False
        
        if self.check_ip_attempts():
            "If we detect too many attempts from the same IP address..."
            return False
        
        self.cleanup()
        return True
    
    def check_credentials(self, type, username, password):
        """
        If we've tried to login here at least three times, just reject
        it. A return of `True` means that we fail.
        """
        key = (type, username, password)
        if key not in self.auth_index:
            self.auth_index[key] = {
                'attempts': 0,
                'most_recent': None
            }
        self.auth_index[key]['attempts'] += 1
        self.auth_index[key]['most_recent'] = datetime.now()
        if self.auth_index[key]['attempts'] >= 3:
            return True
        return False
    
    def check_ip_attempts(self, ip_address):
        if ip_address is None:
            return False
        if ip_address not in self.ip_index:
            self.ip_index = {
                'attempts': 0,
                'most_recent': None
            }
        self.ip_index[ip_address]['attempts'] += 1
        self.ip_index[ip_address]['most_recent'] = datetime.now()
        
        if self.ip_index[ip_address]['attempts'] >= self.ip_attempt_limit:
            return True
        
        return False
    
    def cleanup(self):
        """
        Remove items from this object if we're too big
        """
        if len(self.ip_index) > self.size:
            ip_addresses = sorted(self.ip_index, key=lambda k: self.ip_index[k]['most_recent'], reverse=True)
            for k in ip_addresses[self.size:]:
                del self.ip_index[k]
        if len(self.auth_index) > self.size:
            credentials = sorted(self.auth_index, key=lambda k: self.auth_index[k]['most_recent'], reverse=True)
            for k in credentials[self.size:]:
                del self.auth_index[k]
        return True