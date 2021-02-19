from neomodel import db, One, ZeroOrOne, StructuredNode, StringProperty, RelationshipFrom, \
    EmailProperty, DateTimeProperty, RelationshipTo, BooleanProperty
import datetime
from typing import Set
from ..interface.user import UserInterface
from ...models.user import User as EUser
from ...models.application import Application as EApplication
from ...models.group import Group as EGroup
from ...util import generate_uuid4
from .application import Application
from .organization import Organization
from .group import Group
from .data import Data
from .apikey import ApiKey


SetUser = Set[EUser]


class User(StructuredNode, UserInterface):
    """
    User Node

    A user cannot exist without being in a Organization (even if that Organization is just "Ian McCarty, Inc")
    A user can belong to only one company
    A company can have multiple users
    A user can be have access to multiple applications, and be in multiple groups
    """
    STATUSES = {'ENABLED': 'Enabled', 'DISABLED': 'Disabled'}
    
    # properties
    uid = StringProperty(unique_index=True, default=generate_uuid4)
    name = StringProperty(required=True)
    email = EmailProperty(required=True, unique_index=True)
    username = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    password_modified_at = DateTimeProperty(default_now=True)
    org_admin = BooleanProperty()
    
    # relationships
    # outgoing relationships
    data = RelationshipTo('.data.Data', 'HAS_DATA')
    organization = RelationshipTo('.organization.Organization', 'IN_ORGANIZATION', cardinality=One)
    applications = RelationshipTo('.application.Application', 'IN_APPLICATION')
    groups = RelationshipTo('.group.Group', 'IN_GROUP')
    apikeys = RelationshipTo('.apikey.ApiKey', 'AUTHENTICATES_USER')
    
    def __init__(self, *args, **kwargs):
        """
        Initialize a User
        
        Set some private properties that can be used as a "cache" for custom queries
        to retrieve some of these objects so that we don't make tons of extra queries
        to pull associated data
        
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self._organization = None
        self._data = list()
        self._apikeys = list()
        self._applications = list()
        self._groups = list()
    
    def get_data(self):
        if not self._data:
            self._data = list(self.data.all())
        return {_x.to_object() for _x in self._data}
    
    def get_organization(self):
        if not self._organization:
            self._organization = self.organization.get_or_none()
        return self._organization.to_object()
    
    def get_applications(self):
        if not self._applications:
            self._applications = list(self.applications.all())
        return {_x.to_object() for _x in self._applications}
    
    def get_groups(self):
        if not self._groups:
            self._groups = list(self.groups.all())
        return {_x.to_object() for _x in self._groups}
    
    def get_apikeys(self):
        if not self._apikeys:
            self._apikeys = list(self.apikeys.all())
        return {_x.to_object() for _x in self._apikeys}
    
    def connect_object(self, relationship, o):
        """
        Maybe I want to use this, but also likely not...
        :param relationship:
        :param o:
        :return:
        """
        r = getattr(self, relationship)
        r.connect(o)
        cached_r = f"_{relationship}"
        cr = getattr(self, cached_r)
        if cr and isinstance(cr, 'list'):
            cr.append(o)
        elif cr and isinstance(cr, None):
            cr = o

    @staticmethod
    def create_from_object(o: EUser) -> EUser:
        """
        Usernames are unique
        uids are unique
        passwords should be hashed (bcrypt)
        password_modified should be autoset
        
        :param o:
        :return:
        """
        _org = o.organization._object
        if not _org:
            _org = Organization.nodes.filter(uid=o.organization.uid)
        
        _apps = [a._object for a in o.applications]
        if not all(_apps):
            _apps = Application.nodes.filter(uid__in=[a.uid for a in o.applications])
            
        _groups = [g._object for g in o.groups]
        if not all(_groups):
            _groups = Group.nodes.filter(uid__in=[g.uid for g in o.groups])
        
        if not o.username:
            raise Exception("A username is required")
        
        with db.transaction:
            _o = User(
                uid=o.uid or generate_uuid4(),
                name=o.name,
                email=o.email,
                username=o.username,
                password=o.password,
                status=o.status,
                created_at=o.created_at,
                modified_at=o.modified_at,
                password_modified_at=o.password_modified_at,
                org_admin=o.org_admin
            )
            _o.save()
            _o.organization.connect(_org)
            _o._organization = _org
            for _a in _apps:
                _o.applications.connect(_a)
                _o._applications.append(_a)
            for _g in _groups:
                _o.groups.connect(_g)
                _o._groups.append(_g)
        
            # attach any data nodes
            for x in o.data:
                _data = Data(
                    key=x.key,
                    value=x.value
                )
                _data.save()
                _data.user.connect(_o)
                _o._data.append(_data)
    
        return _o.to_object(organization_flag=True, application_flag=True, group_flag=True, apikey_flag=True)
    
    @staticmethod
    def get_object(o: EUser):
        if not o._object:
            o._object = User.nodes.get(uid=o.uid)  # will raise exception if not found
        return o._object
    
    @staticmethod
    def attach_application(o: EUser, a: EApplication) -> EUser:
        """
        Attach an Application to a User
        
        :param o:
        :param a:
        :return:
        """
        _o = User.get_object(o)
        _a = Application.get_object(a)
        _o.applications.connect(_a)
        _o._applications.append(_a)
        return o
    
    @staticmethod
    def detach_application(o: EUser, a: EApplication) -> EUser:
        """
        Detach an Application from a User - this also removes
        a User from group memberships from that Application
        
        :param o:
        :param a:
        :return:
        """
        with db.transaction:
            _o = User.get_object(o)
            _a = Application.get_object(a)
            
            # remove from any groups associated with the app
            for _g in _a.groups.all():
                _o.groups.disconnect(_g)
                if _g in _o._groups:
                    _o._groups.remove(_g)
            
            # disconnect from the app
            _o.applications.disconnect(_a)
            if _a in _o._applications:
                _o._applications.remove(_a)
        return o
    
    @staticmethod
    def attach_group(o: EUser, g: EGroup) -> EUser:
        """
        Attach a Group to a User
        
        Note: The User must already be a member of the associated Application
        
        :param o:
        :param g:
        :return:
        """
        _o = User.get_object(o)
        _g = Group.get_object(g)
        
        member_application_ids = {x.uid for x in _o.applications.all()}
        group_application_id = _g.application.get().uid
        if group_application_id not in member_application_ids:
            raise Exception("User must be a member of application %s to join group %s" % (group_application_id, g.id))
        
        _o.groups.connect(_g)
        _o._groups.append(_g)
        return o
    
    @staticmethod
    def detach_group(o: EUser, g: EGroup) -> EUser:
        """
        Detach a Group from a User
        
        :param o:
        :param g:
        :return:
        """
        with db.transaction:
            _o = User.get_object(o)
            _g = Group.get_object(g)
            _o.groups.disconnect(_g)
            if _g in _o._groups:
                _o._groups.remove(_g)
        return o
    
    @staticmethod
    def update_from_object(o: EUser) -> EUser:
        if not o.edits:
            return o
        
        _o = User.get_object(o)
        with db.transaction:
            local_fields = {'name', 'username', 'email', 'password', 'status', 'org_admin'}
            local_field_edits = {(s[0], s[1]) for s in o.edits if s[0] in local_fields}
            if local_field_edits:
                for field, new_value in local_field_edits:
                    setattr(_o, field, new_value)
                _o.modified_at = datetime.datetime.now()
                _o.save()
            
            foreign_fields = {'data', }
            foreign_field_edits = {s[0]: s[1] for s in o.edits if s[0] in foreign_fields}
            if foreign_field_edits:
                # CRUD on data
                Data.update_data_nodes(foreign_field_edits.get('data'), _o, 'user')
        
        return _o.to_object(organization_flag=True, application_flag=True, group_flag=True, apikey_flag=True)
    
    def to_object(self, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) -> EUser:
        o = EUser(
            uid=self.uid,
            name=self.name,
            email=self.email,
            username=self.username,
            password=self.password,
            status=self.status,
            created_at=self.created_at,
            modified_at=self.modified_at,
            password_modified_at=self.password_modified_at,
            org_admin=self.org_admin
        )
        o.data = {_data.to_object() for _data in self.data.all()}
        
        if organization_flag:
            o.organization = self.get_organization()
        
        if application_flag:
            o.applications = self.get_applications()
        
        if group_flag:
            o.groups = self.get_groups()

        if apikey_flag:
            o.apikeys = self.get_apikeys()

        o._object = self
        return o
    
    @staticmethod
    def get_all(organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, limit=25, offset=0, order_by='email', *args, **kwargs) -> SetUser:
        orgs = [x.to_object(
                            organization_flag=organization_flag,
                            application_flag=application_flag,
                            group_flag=group_flag,
                            apikey_flag=apikey_flag)
            for x in User.nodes.order_by(order_by)[offset:offset+limit]
        ]
        return orgs
    
    @staticmethod
    def get_by_uid(uid, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) -> EUser:
        """
        Retrieve a User based on its ID

        :param uid:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        user = None
        _user = User.nodes.get_or_none(uid=uid)
        if _user:
            user = _user.to_object(organization_flag=organization_flag, application_flag=application_flag, group_flag=group_flag, apikey_flag=apikey_flag)
        return user
    
    @staticmethod
    def get_by_username(username, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, *args, **kwargs) -> EUser:
        """
        Retrieve a User based on its username

        :param username:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        user = None
        _user = User.nodes.get_or_none(username=username)
        if _user:
            user = _user.to_object(organization_flag=organization_flag, application_flag=application_flag, group_flag=group_flag, apikey_flag=apikey_flag)
        return user
    
    @staticmethod
    def search(search, organization_flag=False, application_flag=False, group_flag=False, apikey_flag=False, limit=25, offset=0, order_by='email', *args, **kwargs) -> SetUser:
        """
        Search for Users
        
        @see documentation for econtextauth.mappers.neo4j.__init__ for instructions on creating the index
        
        :param search:
        :param organization_flag:
        :param application_flag:
        :param group_flag:
        :param apikey_flag:
        :param args:
        :param kwargs:
        :return:
        """
        users_dict = dict()
        ordered_user_ids = list()
        users = list()
        params = {
            'search_term': search
        }
        
        # full-text search against organizations and users
        query = "CALL db.index.fulltext.queryNodes('broad_search_index', $search_term) YIELD node, score " \
                "OPTIONAL MATCH (node:Organization)<-[:IN_ORGANIZATION]-(u:User) " \
                "RETURN node, u"
        results, meta = db.cypher_query(query, params)
        for node, u in results:
            # user match (name, email, username)
            if "User" in node.labels and node['uid'] not in users_dict:
                users_dict[node['uid']] = User.inflate(node)
            if u and u['uid'] not in users_dict:
                users_dict[u['uid']] = User.inflate(u)
        
        # substring matches against API keys
        query = "MATCH (k:ApiKey)<--(u:User) WHERE k.key CONTAINS $search_term RETURN u"
        results, meta = db.cypher_query(query, params)
        for (u,) in results:
            if u and u['uid'] not in users_dict:
                users_dict[u['uid']] = User.inflate(u)
        
        # populate Users with appropriate info
        query = "MATCH (u:User)-->(n) WHERE u.uid IN $user_ids RETURN u.uid, n"
        results, meta = db.cypher_query(query, {'user_ids': list(users_dict.keys())})
        for uid, node in results:
            user = users_dict.get(uid)
            if "Organization" in node.labels:
                user._organization = Organization.inflate(node)
            elif "Application" in node.labels:
                user._applications.append(Application.inflate(node))
            elif "Group" in node.labels:
                user._groups.append(Group.inflate(node))
            elif "ApiKey" in node.labels:
                user._apikeys.append(ApiKey.inflate(node))
                
        return {
            u.to_object(organization_flag=organization_flag, application_flag=application_flag, group_flag=group_flag,
                        apikey_flag=apikey_flag) for u in users_dict.values()}
    
    @staticmethod
    def delete_from_object(o: EUser) -> bool:
        _o = User.get_object(o)
        with db.transaction:
            # delete associated data nodes first:
            for data in _o.data.all():
                data.delete()
            _o.delete()
        return True
