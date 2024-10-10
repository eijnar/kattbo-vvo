from sqlalchemy import Table, Column, Integer, UUID, ForeignKey

from core.database.base import Base


group_users = Table('group_users', Base.metadata,
                    Column('users_id', UUID, ForeignKey(
                        'users.id'), primary_key=True),
                    Column('role_id', Integer, ForeignKey(
                        'groups.id'), primary_key=True)
                    )
