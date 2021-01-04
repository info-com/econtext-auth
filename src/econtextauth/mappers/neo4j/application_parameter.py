from neomodel import StructuredNode, JSONProperty, StringProperty, RelationshipFrom

from ..interface.application_parameter import ApplicationParameterInterface
from ...models.application_parameter import ApplicationParameter as EApplicationParameter


class ApplicationParameter(StructuredNode, ApplicationParameterInterface):
    """
    ApplicationParameter

    Similar to data - this Node defines a possible key->value pair that may
    be filled by a Data node associated with a User. So, for example, the
    application for the "eContext API" may have an ApplicationParameter that
    defines a "tier_depth" parameter. The user may then use a Data node
    attached to both the User and to the Application to provide a user value
    for that parameter.
    """
    # properties
    key = StringProperty(required=True)
    datatype = StringProperty(required=True)
    default = JSONProperty(default=None)
    description = StringProperty()
    
    # relationships
    # outgoing relationships (may or may not exist)
    application = RelationshipFrom('.application.Application', 'HAS_PARAMETER')
    
    def to_object(self, *args, **kwargs) -> EApplicationParameter:
        application_parameter = EApplicationParameter(
            key=self.key,
            datatype=self.datatype,
            default=self.default,
            description=self.description
        )
        application_parameter._object = self
        return application_parameter
    
    @staticmethod
    def update_param_node(new_params, db_object, relationship):
        if not hasattr(db_object, 'parameters') or not new_params:
            return
        
        existing_params = {d.to_object() for d in db_object.parameters.all()}
        existing_params_dict = {d.key: d for d in existing_params}
        for param_node in new_params:
            # they're the same
            if param_node in existing_params:
                continue
            # new values
            if param_node.key in existing_params_dict:
                existing_node = existing_params_dict.get(param_node.key)
                existing_node._object.datatype = param_node.datatype
                existing_node._object.default = param_node.default
                existing_node._object.description = param_node.description
                existing_node._object.save()
            # new node
            else:
                param_node._object = ApplicationParameter(
                    key=param_node.key,
                    datatype=param_node.datatype,
                    default=param_node.default,
                    description=param_node.description
                )
                param_node._object.save()
                rel = getattr(param_node._object, relationship)
                rel.connect(db_object)
        # deletions
        existing_params_keys = set(existing_params_dict.keys())
        new_params_keys = {d.key for d in new_params}
        deletions = new_params_keys.difference(existing_params_keys)
        for key in deletions:
            existing_params_dict[key]._object.delete()
