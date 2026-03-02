from datetime import datetime
from typing import Optional, Dict, TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, func, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from .base import Base

if TYPE_CHECKING:
    from resource import Resource

class Module(Base):
    """
    Topics Units within a learning path
    

    A module contains multiple resources
    A learning path contains multiple modules
    """

    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    learning_path_id: Mapped[int] = mapped_column(ForeignKey("learning_paths.id", ondelete='CASCADE'), index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    order_index: Mapped[int] = mapped_column(index=True)
    duration_days: Mapped[Optional[int]]
    prereqs_json: Mapped[Optional[dict]] = mapped_column(JSON)
    learning_objectives: Mapped[Optional[dict]] = mapped_column(JSON,nullable=True,)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    learning_path = relationship("LearningPath", back_populates="modules")
    learning_resources = relationship(
        "LearningResource",
        back_populates="module",
        cascade="all, delete-orphan",
        lazy="dynamic",
        order_by="LearningResource.order_index"
    )

    def __repr__(self):
        return f"<Module(id={self.id}, name={self.name}, order={self.order_index})>"

    def __str__(self):
        return self.name

    @property
    def learning_resource_count(self) -> int:
        "Get the total number of resources across this module"
        return self.learning_resources.count()

    @classmethod
    def create(
        cls, 
        name: str, 
        learning_path_id: int, 
        order_index: int, 
        description: Optional[str]=None,
        duration_days: Optional[int]=None, 
        prereqs_json: Optional[dict]=None, 
        learning_objectives: Optional[dict]=None, 
        ) -> "Module":
        """
        Factory method to create a new module.
        
        Args:
            name (str): The name of the module
            learning_path (str, foreign_key): The id of the learning path the module belongs to
            order_index (int): Number indicating sequence the module falls in the learning path
            description (str, optional): Detailed description
            duration_days (int, optional): Expected completion time
            prereqs_json (jsonb, optional): Other modules required completion before starting this module
            learning_objectives (str, optional): Learning goals for the module            
            learning_resource_count: Number of resources in this module
            
        Returns:
            Module: A new Module instance
        """
        return cls(
            name=name,
            learning_path_id=learning_path_id,
            order_index=order_index,
            description=description,
            duration_days=duration_days,
            prereqs_json=prereqs_json,
            learning_objectives=learning_objectives,
        )

    def update_info(self, name=None, learning_path=None, order_index=None, description=None, duration_days=None, prereqs_json=None, learning_objectives=None, learning_resource_count=None):
        if name is not None:
            self.name = name
        if learning_path is not None:
            self.learning_path = learning_path
        if order_index is not None:
            self.order_index = order_index
        if description is not None:
            self.description = description
        if duration_days is not None:
            self.duration_days = duration_days
        if prereqs_json is not None:
            self.prereqs_json = prereqs_json
        if learning_objectives is not None:
            self.learning_objectives = learning_objectives
        if learning_resource_count is not None:
            self.learning_resource_count = learning_resource_count
