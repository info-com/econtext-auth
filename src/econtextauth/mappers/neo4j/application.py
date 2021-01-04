from neomodel import db, StructuredNode, StringProperty, DateTimeProperty, \
    RelationshipFrom, RelationshipTo
import datetime
from typing import Set
from .application_parameter import ApplicationParameter
from .data import Data
from ..interface.application import ApplicationInterface
from ...models.application import Application as EApplication
from ...util import generate_uuid4

SetApplication = Set[EApplication]


class Application(StructuredNode, ApplicationInterface):
    """
    An Application represents an Entity that may be "logged into"
    """
    STATUSES = {'ENABLED': 'Enabled', 'DISABLED': 'Disabled'}
    
    # properties
    uid = StringProperty(unique_index=True, default=generate_uuid4)
    name = StringProperty(unique_index=True, required=True)
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    description = StringProperty()
    jwt_secret = StringProperty(default=generate_uuid4)
    
    # relationships
    # incoming
    parameters = RelationshipTo('.application_parameter.ApplicationParameter', 'HAS_PARAMETER')
    data = RelationshipTo('.data.Data', 'HAS_DATA')
    
    # outgoing
    groups = RelationshipFrom('.group.Group', 'HAS_APPLICATION')
    users = RelationshipFrom('.user.User', 'IN_APPLICATION')
    
    def to_object(self, group_flag=False, user_flag=False, *args, **kwargs) -> EApplication:
        app = EApplication(
            uid=self.uid,
            name=self.name,
            description=self.description,
            status=self.status,
            jwt_secret=self.jwt_secret,
            created_at=self.created_at,
            modified_at=self.modified_at
        )
        app.data = {x.to_object() for x in self.data.all()}
        app.parameters = {x.to_object() for x in self.parameters.all()}
        
        if group_flag:
            app.groups = {x.to_object() for x in self.groups.all()}
        
        if user_flag:
            app.users = {x.to_object() for x in self.users.all()}
        
        app._object = self
        return app
    
    @staticmethod
    def get_object(o: EApplication):
        if not o._object:
            o._object = Application.nodes.get(uid=o.uid)  # will raise exception if not found
        return o._object
    
    @staticmethod
    def get_by_uid(uid, group_flag=False, user_flag=False, *args, **kwargs) -> EApplication:
        """
        Retrieve an Application based on its ID
        
        :param uid:
        :return:
        """
        app = None
        _app = Application.nodes.get_or_none(uid=uid)
        if _app:
           app = _app.to_object(group_flag=group_flag, user_flag=user_flag)
        return app
    
    @staticmethod
    def get_by_uids(uids, group_flag=False, user_flag=False, *args, **kwargs) -> SetApplication:
        """
        Retrieve an Application based on its ID
        
        :param uid:
        :return:
        """
        if not uids:
            return set()
        _apps = Application.nodes.filter(uid__in=tuple(uids))
        return {o.to_object(group_flag=group_flag, user_flag=user_flag) for o in _apps}
    
    @staticmethod
    def get_all(group_flag=False, user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        apps = [
            x.to_object(group_flag=group_flag, user_flag=user_flag) for x in Application.nodes.order_by(order_by)[offset:offset+limit]
        ]
        return apps
    
    @staticmethod
    def create_from_object(app: EApplication) -> EApplication:
        with db.transaction:
            _app = Application(
                uid=app.uid or generate_uuid4(),
                name=app.name,
                description=app.description,
                status=app.status,
                created_at=app.created_at,
                modified_at=app.modified_at,
                jwt_secret=app.jwt_secret or generate_uuid4()
            )
            _app.save()
            
            # attach any parameters
            for x in app.parameters:
                _p = ApplicationParameter(
                    key=x.key,
                    datatype=x.datatype,
                    default=x.default,
                    description=x.description
                )
                _p.save()
                _p.application.connect(_app)
            
            # attach any data nodes
            for x in app.data:
                _data = Data(
                    key=x.key,
                    value=x.value
                )
                _data.save()
                _data.application.connect(_app)
        
        return _app.to_object()
    
    @staticmethod
    def update_from_object(o: EApplication) -> EApplication:
        if not o.edits:
            return o
        
        _o = Application.get_object(o)
        with db.transaction:
            local_fields = {'name', 'description', 'status', 'jwt_secret'}
            local_field_edits = {(s[0], s[1]) for s in o.edits if s[0] in local_fields}
            if local_field_edits:
                for field, new_value in local_field_edits:
                    setattr(_o, field, new_value)
                _o.modified_at = datetime.datetime.now()
                _o.save()
            
            foreign_fields = {'data', 'parameters'}
            foreign_field_edits = {s[0]: s[1] for s in o.edits if s[0] in foreign_fields}
            if foreign_field_edits:
                # CRUD on data
                Data.update_data_nodes(foreign_field_edits.get('data'), _o, 'application')
                
                # CRUD on parameters
                ApplicationParameter.update_param_node(foreign_field_edits.get('parameters'), _o, 'application')
        
        return _o.to_object()
    
    @staticmethod
    def delete_from_object(o: EApplication) -> bool:
        _o = Application.get_object(o)
        with db.transaction:
            # delete associated parameters and data nodes first:
            for data in _o.data.all():
                data.delete()
                
            for param in _o.parameters.all():
                param.delete()
            
            # also need to remove groups, else those will be stranded...
            for group in _o.groups.all():
                group.delete()
            _o.delete()
        
        return True