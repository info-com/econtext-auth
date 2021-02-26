from neomodel import db, StringProperty, RelationshipFrom, \
    DateTimeProperty, One, StructuredNode
import datetime
from ...mappers.interface.apikey import ApiKeyInterface
from ...models.apikey import ApiKey as EApiKey
from ...util import generate_key, generate_secret, hash_secret


class ApiKey(StructuredNode, ApiKeyInterface):
    """
    ApiKey Node
    
    Provides credentials that may be used to authenticate a User
    """
    
    STATUSES = {'DISABLED': 'Disabled', 'ENABLED': 'Enabled'}
    
    # properties
    key = StringProperty(unique_index=True, required=True)
    secret = StringProperty(required=True)  # bcrypted base64 uuid4 (econtextauth.util.generate_secret
    name = StringProperty()
    description = StringProperty()
    status = StringProperty(default="ENABLED", choices=STATUSES)
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)
    
    # relationships
    user = RelationshipFrom('.user.User', 'AUTHENTICATES_USER', cardinality=One)
    
    def to_object(self, user_flag=True, *args, **kwargs) -> EApiKey:
        apikey = EApiKey(
            key=self.key,
            secret=self.secret,
            name=self.name,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )
        if user_flag:
            user = self.user.get()
            apikey.user = user.to_object()
        apikey._object = self
        return apikey
    
    @staticmethod
    def get_object(o: EApiKey):
        if not o._object:
            o._object = ApiKey.nodes.get(key=o.key)  # will raise exception if not found
        return o._object
    
    @staticmethod
    def get_apikeys_by_userids(userids: list):
        """
        Return a list of ApiKeys
        """
        query = "MATCH (k:ApiKey)<-[:AUTHENTICATES_USER]-(u:User) WHERE u.uid IN $user_ids RETURN u.uid, k"
        results, meta = db.cypher_query(query, {'user_ids': userids})
        apikeys = list()
        for uid, key in results:
            apikeys.append((uid, ApiKey.inflate(key)))
        return [(uid, o.to_object(user_flag=False)) for uid, o in apikeys]
    
    @staticmethod
    def get_by_key(key, *args, **kwargs) -> EApiKey:
        """
        Return an ApiKey model identified by the specified key
        
        :param key:
        :param args:
        :param kwargs:
        :return:
        """
        o = None
        _o = ApiKey.nodes.get_or_none(key=key)
        if _o:
            o = _o.to_object()
        return o
    
    @staticmethod
    def create_from_object(o: EApiKey) -> EApiKey:
        """
        Create a new ApiKey
        
        :param o:
        :return:
        """
        _u = o.user._object
        if not _u:
            raise Exception("No user specified for ApiKey")
        
        secret = o.secret or generate_secret()
        with db.transaction:
            _o = ApiKey(
                key=o.key or generate_key(),
                secret=hash_secret(secret),
                name=o.name,
                description=o.description,
                status=o.status,
                created_at=o.created_at,
                modified_at=o.modified_at
            )
            _o.save()
            _o.user.connect(_u)
        
        # reset the secret to the pre-hashed secret - this is the last time we'll see this
        _o.secret = secret
        return _o.to_object()
    
    @staticmethod
    def delete_from_object(o: EApiKey) -> bool:
        _o = ApiKey.get_object(o)
        with db.transaction:
            _o.delete()
        return True
    
    @staticmethod
    def update_from_object(o: EApiKey) -> EApiKey:
        if not o.edits:
            return o
        
        _o = ApiKey.get_object(o)
        with db.transaction:
            local_fields = {'name', 'description', 'status'}
            local_field_edits = {(s[0], s[1]) for s in o.edits if s[0] in local_fields}
            if local_field_edits:
                for field, new_value in local_field_edits:
                    setattr(_o, field, new_value)
                _o.modified_at = datetime.datetime.now()
                _o.save()
        
        return _o.to_object()

