from sqlalchemy import Table, Column, Integer, ForeignKey

from core.database.base import Base


role_users = Table('role_users', Base.metadata,
                    Column('users_id', Integer, ForeignKey(
                        'users.id'), primary_key=True),
                    Column('role_id', Integer, ForeignKey(
                        'roles.id'), primary_key=True)
                    )
