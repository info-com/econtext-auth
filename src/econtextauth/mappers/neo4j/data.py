from neomodel import StructuredNode, JSONProperty, StringProperty, ZeroOrOne, RelationshipTo, RelationshipFrom
from ..interface.data import DataInterface
from ...models.data import Data as EData

import logging
log = logging.getLogger('econtext')


class Data(StructuredNode, DataInterface):
    """
    Data Node
    
    The Data node provides arbitrary data in a key->value scheme and may be
    applicable to a user directly, or in relation to an application as well.
    """
    # properties
    key = StringProperty(required=True)
    value = JSONProperty()
    
    # relationships
    # outgoing relationships (may or may not exist)
    applies_to_application = RelationshipTo('.application.Application', 'APPLIES_TO', cardinality=ZeroOrOne)
    
    # incoming relationships (should only ever be one of these)
    user = RelationshipFrom('.user.User', 'HAS_DATA', cardinality=ZeroOrOne)
    application = RelationshipFrom('.application.Application', 'HAS_DATA', cardinality=ZeroOrOne)
    organization = RelationshipFrom('.organization.Organization', 'HAS_DATA', cardinality=ZeroOrOne)
    group = RelationshipFrom('.group.Group', 'HAS_DATA', cardinality=ZeroOrOne)
    
    def to_object(self, *args, **kwargs) -> EData:
        data = EData(
            key=self.key,
            value=self.value
        )
        data._object = self
        return data
    
    @staticmethod
    def update_data_nodes(new_data, db_object, relationship):
        """
        Update data nodes
        
        :param new_data:
        :param db_object:
        :param relationship: The name of the attribute defining the relationship to connect the data node to
        :return:
        """
        if not hasattr(db_object, 'data') or not new_data:
            return
        
        existing_data = {d.to_object() for d in db_object.data.all()}
        existing_data_dict = {d.key: d for d in existing_data}
        for data_node in new_data:
            # they're the same
            if data_node in existing_data:
                continue
            # new value
            if data_node.key in existing_data_dict:
                existing_node = existing_data_dict.get(data_node.key)
                existing_node._object.value = data_node.value
                existing_node._object.save()
            # new node
            else:
                if data_node.key == '':
                    continue
                data_node._object = Data(
                    key=data_node.key,
                    value=data_node.value
                )
                data_node._object.save()
                rel = getattr(data_node._object, relationship)
                rel.connect(db_object)
        # deletions
        existing_data_keys = set(existing_data_dict.keys())
        new_data_keys = {d.key for d in new_data}
        deletions = existing_data_keys.difference(new_data_keys)
        for key in deletions:
            existing_data_dict[key]._object.delete()
