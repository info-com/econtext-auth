"""
Migration scripts for moving from an old database (rethinkdb) into Neo4j

Organizations need to imported before Users may be added in. For the
RethinkDB version of eContextAuth, there was no concept of an
"Organization" so these will need to be manually generated first.

"""
import json
from collections import defaultdict
from neomodel import config as neo_config

from .... import models
from ....mappers import neo4j
from ....util import parse_datetime
import argparse
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

try:
    import remodel
    from remodel.models import Model
except:
    raise ImportError("Could not import remodel - go ahead and manually install remodel in this path to run this migration")


class User(Model):
    has_and_belongs_to_many = ("Application", "Group")
    has_many = ("ApiKey",)


class ApiKey(Model):
    belongs_to = ("User",)


class Group(Model):
    belongs_to = ("Application",)
    has_and_belongs_to_many = ("User",)


class Application(Model):
    has_and_belongs_to_many = ("User", "Group")


def new_application(mapper, object_dict):
    """
    Create a new Application

    :param mapper:
    :param object_dict:
    :return:
    """
    if not object_dict.get('custom_data'):
        object_dict['custom_data'] = dict()
    o = models.application.Application(
        uid=object_dict.get('id'),
        name=object_dict.get('name'),
        description=object_dict.get('description'),
        status=object_dict.get('status', 'ENABLED'),
        jwt_secret=object_dict.get('jwt_secret'),
        created_at=parse_datetime(object_dict.get('created_at')),
        modified_at=parse_datetime(object_dict.get('modified_at'))
    )
    for k, v in object_dict.get('custom_data').items():
        if v is not None:
            o.data.add(models.data.Data(
                key=k,
                value=v
            ))
    for data_item in object_dict.get('data', list()):
        o.data.add(models.data.Data(**data_item))
    
    for parameter in object_dict.get('parameters', list()):
        o.parameters.add(models.application_parameter.ApplicationParameter(**parameter))
    
    o = mapper.application.Application.create_from_object(o)
    return o


def new_group(mapper, object_dict):
    """
    Create a new Group

    :param mapper:
    :param object_dict:
    :return:
    """
    if not object_dict.get('custom_data'):
        object_dict['custom_data'] = dict()
    
    o = models.group.Group(
        uid=object_dict.get('id'),
        name=object_dict.get('name'),
        description=object_dict.get('description'),
        status=object_dict.get('status', 'ENABLED'),
        application=object_dict.get('application'),
        created_at=parse_datetime(object_dict.get('created_at')),
        modified_at=parse_datetime(object_dict.get('modified_at'))
    )
    for k, v in object_dict.get('custom_data').items():
        if v is not None:
            o.data.add(models.data.Data(
                key=k,
                value=v
            ))
    for data_item in object_dict.get('data', list()):
        o.data.add(models.data.Data(**data_item))
    
    o = mapper.group.Group.create_from_object(o)
    return o


def new_apikey(mapper, object_dict, u):
    """
    POST a new ApiKey and attach it to a User - create

    :param mapper:
    :param object_dict:
    :param u:
    """
    _o = mapper.apikey.ApiKey(
        key=object_dict.get('key'),  # usually empty
        secret=object_dict.get('secret'),  # usually empty
        name=object_dict.get('name'),
        description=object_dict.get('description'),
        status=object_dict.get('status', 'ENABLED'),
        created_at=object_dict.get('created_at'),
        modified_at=object_dict.get('modified_at')
    )
    _o.save()
    _o.user.connect(u._object)
    return True


def new_user(mapper, object_dict):
    """
    Create a new User

    :param mapper:
    :param object_dict:
    :return:
    """
    if not object_dict.get('custom_data'):
        object_dict['custom_data'] = dict()
    
    # pull in related nodes
    _org_id = object_dict.get('organization', None)
    _application_ids = set(object_dict.get('applications', list()))
    _group_ids = set(object_dict.get('groups', list()))
    
    org = mapper.organization.Organization.get_by_uid(_org_id)
    applications = mapper.application.Application.get_by_uids(_application_ids)
    groups = mapper.group.Group.get_by_uids(_group_ids)
    
    application_ids = {o.uid for o in applications}
    group_ids = {o.uid for o in groups}
    
    if not org:
        raise Exception(f"Organization not found: {_org_id}")
    
    if _application_ids.difference(application_ids):
        raise Exception("Some applications not found: %s" % json.dumps(_application_ids.difference(application_ids)))
    
    if _group_ids.difference(group_ids):
        raise Exception("Some groups not found: %s" % json.dumps(_group_ids.difference(group_ids)))
    
    o = models.user.User(
        uid=object_dict.get('id'),
        name=object_dict.get('name', '').strip(),
        email=object_dict.get('email', '').strip(),
        username=object_dict.get('username', '').strip(),
        status=object_dict.get('status', 'ENABLED'),
        created_at=parse_datetime(object_dict.get('created_at')),
        modified_at=parse_datetime(object_dict.get('modified_at')),
        org_admin=object_dict.get('org_admin', True)
    )
    o.password = object_dict.get('password', '').strip()
    
    o.organization = org
    o.applications = applications
    o.groups = groups
    
    for k, v in object_dict.get('custom_data', dict()).items():
        
        # we can eliminate these...
        if k in {'company_id', 'encrypt_key', 'amember_link', 'company_name'}:
            continue
        
        if v is not None:
            o.data.add(models.data.Data(
                key=k,
                value=v
            ))
    for data_item in object_dict.get('data', list()):
        o.data.add(models.data.Data(**data_item))
    
    o = mapper.user.User.create_from_object(o)
    
    # add in api keys
    for api_dict in object_dict.get('apikeys', list()):
        k = new_apikey(mapper, api_dict, o)
    
    return o


def process_applications(mapper):
    """
    Pull objects from RethinkDb and publish them into Neo4j

    :param mapper: econtextauth.mappers.neo4j
    :return:
    """
    old_applications = list(Application.all())
    applications = list()
    for app in old_applications:
        app_dict = app.fields.as_dict()
        applications.append(new_application(mapper, app_dict))
    return applications


def process_groups(mapper):
    """
    Pull objects from RethinkDb and publish them into Neo4j

    :param mapper: econtextauth.mappers.neo4j
    :return:
    """
    old_groups = list(Group.all())
    groups = list()
    for group in old_groups:
        group_dict = group.fields.as_dict()
        group_dict['application'] = group_dict['application_id']
        groups.append(new_group(mapper, group_dict))
    return groups


def process_organizations(mapper, users_list):
    organizations = dict()
    user_email_to_organization_name = dict()  # email to organization_name
    
    for u in users_list:
        cn, ed = find_organization(u)
        user_email_to_organization_name[u.get('email')] = cn
        cd = parse_datetime(u.get('created_at'))
        org = models.organization.Organization(name=cn, created_at=cd)
        custom_data = u.get('custom_data') or dict()

        for k, v in custom_data.items():
            if v is not None:
                org.data.add(models.data.Data(
                    key=k,
                    value=v
                ))
        
        if cn == 'eContext.ai':
            org.uid = '9999999'
        elif 'company_id' in custom_data:
            org.uid = custom_data.get('company_id')
        else:
            org.uid = u.get('id')
        
        if cn in organizations:
            org = organizations[cn]
            if cd < org.created_at:
                org.created_at = cd
        else:
            organizations[cn] = org
    
    old_organizations = organizations
    organizations = dict()
    for o in old_organizations.values():
        organizations[o.name] = mapper.organization.Organization.create_from_object(o)
    return organizations, user_email_to_organization_name


def find_organization(user):
    """
    Look at the company_name and the email address
    """
    econtext_domains = {'Info.com', 'info.com', 'econtext.com', 'econtext.ai'}
    econtext_names = {'info.com', 'econtext', 'econtext.ai', 'econtext.com'}
    email_domain = user.get('email').split("@")[1]
    company_name = (user.get('custom_data') or dict()).get('company_name')
    if company_name and company_name.lower() in econtext_names:
        company_name = 'eContext.ai'
    
    if not company_name:
        if email_domain in econtext_domains:
            company_name = 'eContext.ai'
        else:
            company_name = email_domain
    return company_name, email_domain


def process_users(mapper):
    new_users = list()
    users = [u for u in User.all()]
    organizations, user_email_to_organization_name = process_organizations(mapper, [u.fields.as_dict() for u in users])
    for u in users:
        user = u.fields.as_dict()
        user['org_admin'] = True
        if user['status'] not in {'ENABLED', 'DISABLED'}:
            user['status'] = 'ENABLED'
        org = organizations.get(user_email_to_organization_name.get(user.get('email')))
        user['organization'] = org.uid
        user['applications'] = [x.fields.id for x in u.fields.applications.all()]
        user['groups'] = [x.fields.id for x in u.fields.groups.all()]
        user['apikeys'] = list()
        for apikey in u.fields.api_keys.all():
            apikey_dict = apikey.fields.as_dict()
            apikey_dict['key'] = apikey_dict['id']
            user['apikeys'].append(apikey_dict)
        new_users.append(new_user(mapper, user))
    return new_users


def main():
    mapper = neo4j
    parser = argparse.ArgumentParser(description='Migrate from RethinkDB to Neo4j.')
    parser.add_argument("--rethink", dest="rethink", default="127.0.0.1", help="RethinkDB Host", metavar="HOST")
    parser.add_argument("--neo", dest="neo", default="bolt://neo4j:neo4j@127.0.0.1:7687", help="Neo4j Host", metavar="HOST")
    parser.add_argument("--reformat", dest="reformat", action='store_true', help="Completely erase the existing db first")
    options = parser.parse_args()
    
    remodel.connection.pool.configure(host=options.rethink, db='econtext_users')
    neo_config.DATABASE_URL = options.neo
    
    if options.reformat:
        mapper.reformat_database()
    
    log.info("Processing Applications")
    applications = process_applications(mapper)
    
    log.info("Processing Groups")
    groups = process_groups(mapper)
    
    log.info("Processing Users")
    users = process_users(mapper)


if __name__ == '__main__':
    main()