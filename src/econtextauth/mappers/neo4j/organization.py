from neomodel import db, StructuredNode, StringProperty, RelationshipFrom, RelationshipTo, DateTimeProperty

import datetime
from .data import Data
from ..interface.organization import OrganizationInterface
from ...models.organization import Organization as EOrganization
from ...util import generate_uuid4
import logging
log = logging.getLogger('econtextauth')


class Organization(StructuredNode, OrganizationInterface):
    """
    Organization Node
    
    A user cannot exist without being in a Organization (even if that Organization is just "Ian McCarty, Inc")
    A user can belong to only one company
    A company can have multiple users
    A user can be have access to multiple applications, and be in multiple groups
    """

    STATUSES = {'ENABLED': 'Enabled', 'DISABLED': 'Disabled'}
    
    # properties
    uid = StringProperty(unique_index=True, default=generate_uuid4)
    name = StringProperty(unique_index=True, required=True)
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    
    # relationships
    # incoming relationships
    users = RelationshipFrom('.user.User', 'IN_ORGANIZATION')
    
    # outgoing relationships
    data = RelationshipTo('.data.Data', 'HAS_DATA')
    
    def to_object(self, user_flag=False, *args, **kwargs) -> EOrganization:
        o = EOrganization(
            uid=self.uid,
            name=self.name,
            status=self.status,
            created_at=self.created_at,
            modified_at=self.modified_at
        )
        o.data = {x.to_object() for x in self.data.all()}
        
        if user_flag:
            o.users = {x.to_object() for x in self.users.all()}
            o.admins = {x.to_object() for x in self.users.filter(org_admin=True)}

        o._object = self
        return o
    
    @staticmethod
    def get_by_uid(uid, user_flag=False, *args, **kwargs) -> EOrganization:
        org = None
        _org = Organization.nodes.get_or_none(uid=uid)
        if _org:
            org = _org.to_object(user_flag=user_flag)
        return org
    
    @staticmethod
    def get_all(user_flag=False, limit=25, offset=0, order_by='name', *args, **kwargs) -> set:
        orgs = [
            x.to_object(user_flag=user_flag) for x in Organization.nodes.order_by(order_by)[offset: offset+limit]
        ]
        return orgs

    @staticmethod
    def create_from_object(o: EOrganization) -> EOrganization:
        with db.transaction:
            _o = Organization(
                uid=o.uid or generate_uuid4(),
                name=o.name,
                status=o.status,
                created_at=o.created_at,
                modified_at=o.modified_at
            )
            _o.save()
        
            # attach any data nodes
            for x in o.data:
                _data = Data(
                    key=x.key,
                    value=x.value
                )
                _data.save()
                _data.organization.connect(_o)
    
        return _o.to_object()

    @staticmethod
    def update_from_object(o: EOrganization) -> EOrganization:
        if not o.edits:
            return o
        
        _o = o._object
        if not _o:
            _o = Organization.nodes.get(uid=o.uid)  # will raise exception if not found
        
        with db.transaction:
            local_fields = {'name', 'status'}
            local_field_edits = {(s[0], s[1]) for s in o.edits if s[0] in local_fields}
            if local_field_edits:
                for field, new_value in local_field_edits:
                    setattr(_o, field, new_value)
                _o.modified_at = datetime.datetime.now()
                _o.save()
        
            foreign_fields = {'data'}
            foreign_field_edits = {s[0]: s[1] for s in o.edits if s[0] in foreign_fields}
            if foreign_field_edits:
                # CRUD on data
                Data.update_data_nodes(foreign_field_edits.get('data'), _o, 'organization')
        
        return _o.to_object()
    
    @staticmethod
    def delete_from_object(o: EOrganization) -> bool:
        _o = o._object
        if not _o:
            _o = Organization.nodes.get(uid=o.uid)  # will raise exception if not found
        
        with db.transaction:
            # delete associated parameters and data nodes first:
            for data in _o.data.all():
                data.delete()
            _o.delete()
        
        return True
