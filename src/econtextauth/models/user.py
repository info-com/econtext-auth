"""
    username = StringProperty(required=True)
    password = StringProperty(required=True)
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    password_modified_at = DateTimeProperty(default_now=True)
    
    # relationships
    # incoming relationships
    admin_for_company = RelationshipFrom('.organization.Organization', 'ADMINISTERS_ORGANIZATION', cardinality=ZeroOrOne)
    
    # outgoing relationships
    data = RelationshipTo('.data.Data', 'HAS_DATA')
    organization = RelationshipTo('.organization.Organization', 'IN_ORGANIZATION', cardinality=One)
    applications = RelationshipTo('.application.Application', 'IN_APPLICATION')
    groups = RelationshipTo('.group.Group', 'IN_GROUP')
    apikeys = RelationshipTo('.apikey.ApiKey', 'AUTHENTICATES_USER')

"""
from .data import Data
from ..util import get_base_url, hash_secret


def password_length_check(password) -> bool:
    """
    Check the length of a password
    :param password:
    :return: True is the password is long enough and raises an exception if not
    """
    if len(password) < 7:
        raise Exception("Password must be at least 7 characters long")
    return True


def password_exists(password) -> bool:
    """
    Check that a password was entered
    :param password:
    :return: True is the password is longer than 1
    """
    if len(password) < 1:
        raise Exception("Password must be included")
    return True


class User(object):
    
    def __init__(self, uid=None, username=None, password=None, name=None, email=None, status=None, created_at=None, modified_at=None, password_modified_at=None, org_admin=False, *args, **kwargs):
        self.uid = uid
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.status = status
        self.created_at = created_at
        self.modified_at = modified_at
        self.password_modified_at = password_modified_at
        self.org_admin = org_admin
        
        self.organization = None    # from another node
        self.apikeys = set()        # from another node
        self.applications = set()   # from other nodes
        self.groups = set()         # from other nodes
        self.data = set()           # from other nodes
        
        self.edits = set()
    
    def build_data_dict(self):
        """
        Return the data fields as a dictionary. This maintains backward
        compatibility with an older version, but should not be relied
        on moving forward. Use the data list instead.
        :return:
        """
        data_dict = {d.key: d.value for d in self.data}
        if self.organization:
            # For backward compatibility on some apps, lets include this in the custom_data output
            data_dict['company_name'] = self.organization.name
            data_dict['encrypt_id'] = self.organization.uid
            data_dict['company_id'] = self.organization.uid
        return data_dict
    
    def to_dict(self):
        """
        Return this object as a dictionary
        :return:
        """
        return {  # base user data
            'id': self.uid,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'custom_data': self.build_data_dict(),
            'href': '{}/api/users/user/{}'.format(get_base_url(), self.uid),
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'password_modified_at': str(self.password_modified_at or ''),
            'status': self.status or 'DISABLED',
            'organization': self.organization.to_dict() if self.organization else None,
            'org_admin': self.org_admin,
            
            # Extra relations
            'data': [x.to_dict() for x in self.data],
            'apikeys': [x.to_dict_minimal() for x in self.apikeys],
            'applications': [x.to_dict() for x in self.applications],
            'groups': [x.to_dict() for x in self.groups]
        }
    
    def to_dict_minimal(self):
        # base user data
        return {
            'id': self.uid,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'custom_data': self.build_data_dict(),
            'href': '{}/api/users/user/{}'.format(get_base_url(), self.uid),
            'created_at': str(self.created_at or ''),
            'modified_at': str(self.modified_at or ''),
            'password_modified_at': str(self.password_modified_at or ''),
            'status': self.status or 'DISABLED',
            'organization': self.organization.to_dict() if self.organization else None,
            'org_admin': self.org_admin
        }
    
    def strip_password(self, password):
        """
        Remove whitespace from a password
        
        :param password:
        :return:
        """
        return password.strip()
    
    def check_password(self, password, policies=None):
        """
        Provide a policy for managing a password - generally, this is just
        a length check for now, but may also include policies that could
        implemented using a series of callbacks functions. The structure of
        the callbacks would be that they accept a single string (password)
        as an input, and return a boolean that indicates that the password
        passed the test
        
        :param policies: a list of callback functions to check the password
        :return:
        """
        if policies is None:
            policies = [password_exists, password_length_check]
        for policy in policies:
            if not policy(password):
                raise Exception("Password failed policy check - please try again with a new password")
        return True
    
    def set_password(self, password, policies=None, *args, **kwargs):
        pw = self.strip_password(password)
        if not self.check_password(pw, policies=policies):
            raise Exception("An error occurred checking the password - please try again")
        self.password = hash_secret(pw)
    
    def set_name(self, new_name):
        if self.name != new_name:
            self.name = new_name
            self.edits.add(('name', new_name))
    
    def set_username(self, new_username):
        if self.username != new_username:
            self.username = new_username
            self.edits.add(('username', new_username))
    
    def set_email(self, new_email):
        if self.email != new_email:
            self.email = new_email
            self.edits.add(('email', new_email))
    
    def set_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.edits.add(('status', new_status))
    
    def set_org_admin(self, new_org_admin):
        if self.new_org_admin != new_org_admin:
            self.org_admin = new_org_admin
            self.edits.add(('org_admin', new_org_admin))
    
    def set_data(self, new_data):
        # new_data = [{'key': 'spam', 'value': 'eggs'}, ...]
        new_data = frozenset(Data(**data) for data in new_data)
        if self.data != new_data:
            self.data = new_data
            self.edits.add(('data', new_data))
    
    def set_custom_data(self, new_data):
        """
        custom_data comes in as a dictionary instead of a list. So,
        first, we change this into a list, and then submit it.
        
        :param new_data:
        :return:
        """
        new_data = [{'key': k, 'value': v} for k, v in new_data.items()]
        return self.set_data(new_data)
