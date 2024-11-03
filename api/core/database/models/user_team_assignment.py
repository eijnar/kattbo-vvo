from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core.database.base import Base


class UserTeamAssignment(Base):
    __tablename__ = 'user_team_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    assigned_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))
    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))

    user = relationship('User', back_populates='user_team_assignments')
    team = relationship('Team', back_populates='user_team_assignments')
    hunting_year = relationship(
        'HuntingYear', back_populates='user_team_assignments')

    __table_args__ = (
        UniqueConstraint('user_id', 'hunting_year_id', name='_user_team_hyear_uc'),
    )
