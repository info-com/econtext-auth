"""
Create our various tables, indexes, etc
"""

from econtextauth.models import *
import rethinkdb as r
import remodel


def create_tables(conn):
    created_tables = r.table_list().run(conn)
    for model_cls in remodel.registry.model_registry.all().values():
        if model_cls._table not in created_tables:
            result = r.table_create(model_cls._table).run(conn)
            if result['tables_created'] != 1:
                raise RuntimeError('Could not create table %s for model %s' % (
                                   model_cls._table, model_cls.__name__))


def create_indexes(conn):
    for model, index_set in remodel.registry.index_registry.all().items():
        model_cls = remodel.registry.model_registry.get(model)
        created_indexes = r.table(model_cls._table).index_list().run(conn)
        for index in index_set:
            if index not in created_indexes:
                result = r.table(model_cls._table).index_create(index).run(conn)
                if result['created'] != 1:
                    raise RuntimeError('Could not create index %s for table %s' % (
                                       index, model_cls._table))
        r.table(model_cls._table).index_wait().run(conn)

