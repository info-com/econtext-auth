from neomodel import db, StructuredNode, StringProperty, DateTimeProperty, \
    RelationshipFrom, RelationshipTo, One
import datetime
from typing import Set
from .application import Application
from .data import Data
from ...util import generate_uuid4
from ..interface.group import GroupInterface
from ...models.group import Group as EGroup


SetGroup = Set[EGroup]


class Group(StructuredNode, GroupInterface):
    """
    A Group node provides access to certain functionality for associated apps
    """
    
    STATUSES = {'ENABLED': 'Enabled', 'DISABLED': 'Disabled'}
    
    # properties
    uid = StringProperty(unique_index=True, default=generate_uuid4)
    name = StringProperty(required=True)
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    description = StringProperty()
    application_id = StringProperty(required=True)
    
    # relationships
    # incoming relationships
    users = RelationshipFrom('.user.User', 'IN_GROUP')
    
    # outgoing relationships
    data = RelationshipTo('.data.Data', 'HAS_DATA')
    application = RelationshipTo('.application.Application', 'HAS_APPLICATION', cardinality=One)
    
    def to_object(self, user_flag=False, *args, **kwargs) -> EGroup:
        group = EGroup(
            uid=self.uid,
            name=self.name,
            description=self.description,
            status=self.status,
            application=self.application_id,
            created_at=self.created_at,
            modified_at=self.modified_at
        )
        group.data = {x.to_object() for x in self.data.all()}
        
        if user_flag:
            group.users = {x.to_object() for x in self.users.all()}
        
        group._object = self
        return group
    
    @staticmethod
    def get_all(user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        orgs = [x.to_object(user_flag=user_flag) for x in Group.nodes.order_by(order_by)[offset:offset+limit]]
        return orgs
    
    @staticmethod
    def get_by_uid(uid, user_flag=False, *args, **kwargs) -> EGroup:
        """
        Retrieve a Group based on its ID
        
        :param uid:
        :return:
        """
        o = None
        _o = Group.nodes.get_or_none(uid=uid)
        if _o:
            o = _o.to_object(user_flag=user_flag)
        return o
    
    @staticmethod
    def get_by_uids(uids, user_flag=False, *args, **kwargs) -> SetGroup:
        """
        Retrieve a set of Groups based on its ID
        
        :param uids:
        :return:
        """
        if not uids:
           return set()
        _groups = Group.nodes.filter(uid__in=tuple(uids))
        return {o.to_object(user_flag=user_flag) for o in _groups}

    @staticmethod
    def create_from_object(o: EGroup) -> EGroup:
        """
        Group names are unique within an Application - so we need to first
        check that we dont' already have a group with the same name in the
        specified application. We'll connect it to this application, so no
        skin off our teeth to pull it here either.
        
        :param o:
        :return:
        """
        _app = Application.nodes.get(uid=o.application)
        for group in _app.groups.all():
            if group.name == o.name.strip():
                raise Exception("A Group with this name already exists for this Application")
        
        with db.transaction:
            _o = Group(
                uid=o.uid or generate_uuid4(),
                name=o.name,
                description=o.description,
                application_id=o.application,
                status=o.status,
                created_at=o.created_at,
                modified_at=o.modified_at
            )
            _o.save()
            _o.application.connect(_app)
        
            # attach any data nodes
            for x in o.data:
                _data = Data(
                    key=x.key,
                    value=x.value
                )
                _data.save()
                _data.group.connect(_o)
    
        return _o.to_object()
    
    @staticmethod
    def get_object(o: EGroup):
        if not o._object:
            o._object = Group.nodes.get(uid=o.uid)  # will raise exception if not found
        return o._object
    
    @staticmethod
    def update_from_object(o: EGroup) -> EGroup:
        if not o.edits:
            return o
        
        _o = Group.get_object(o)
        _app = _o.application.get()
        if 'name' in {s[0] for s in o.edits}:
            for group in _app.groups.all():
                if group.name == o.name.strip() and group.uid != _o.uid:
                    raise Exception("A Group with this name already exists for this Application")
        
        with db.transaction:
            local_fields = {'name', 'description', 'status'}
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
                Data.update_data_nodes(foreign_field_edits.get('data'), _o, 'group')
        
        return _o.to_object()
    
    @staticmethod
    def delete_from_object(o: EGroup) -> bool:
        _o = Group.get_object(o)
        with db.transaction:
            # delete associated data nodes first:
            for data in _o.data.all():
                data.delete()
            _o.delete()
        return True
