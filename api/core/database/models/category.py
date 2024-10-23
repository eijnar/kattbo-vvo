import uuid

from sqlalchemy import String, Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base


class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey(
        'categories.id'), nullable=True)
    parent = relationship("Category", remote_side=[
                          id], backref="subcategories")

    context = Column(String, nullable=False)


class WaypointCategoryMetadataModel(Base):
    __tablename__ = 'waypoint_category_metadata'

    category_id = Column(UUID(as_uuid=True), ForeignKey(
        'categories.id'), primary_key=True)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

    category = relationship("CategoryModel", backref="waypoint_metadata")
