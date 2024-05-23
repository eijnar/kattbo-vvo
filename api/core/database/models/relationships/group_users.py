from sqlalchemy import Table, Column, Integer, ForeignKey

from core.database.base import Base


group_users = Table('group_users', Base.metadata,
                    Column('users_id', Integer, ForeignKey(
                        'users.id'), primary_key=True),
                    Column('role_id', Integer, ForeignKey(
                        'groups.id'), primary_key=True)
                    )
