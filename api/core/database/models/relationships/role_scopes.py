from sqlalchemy import Table, Column, ForeignKey

from core.database.base import Base


role_scopes = Table('role_scopes', Base.metadata,
                     Column('role_id', ForeignKey(
                         'roles.id'), primary_key=True),
                     Column('scope_id', ForeignKey(
                         'scopes.id'), primary_key=True)
                     )
