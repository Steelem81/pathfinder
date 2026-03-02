from .base import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ResourceProgress(Base):

    __tablename__= 'resource_progress'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    learning_resource_id: Mapped[int] = mapped_column(ForeignKey("learning_resources.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(default='not_started')
    started_at: Mapped[Optional[datetime]]
    completed_at: Mapped[Optional[datetime]]
    time_spent_mins: Mapped[Optional[int]]
    notes: Mapped[Optional[str]]
    rating: Mapped[Optional[int]]
    understand_level: Mapped[Optional[float]]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    learning_resource: Mapped["LearningResource"] = relationship(back_populates="resource_progress")
    
    @classmethod
    def create(
        cls,
        learning_resource_id: int,
        status: str="not_started"
    ) -> "ResourceProgress":
        """
        Creates a record to track the progress of an individual resource.

        Args:
        learning_resource_id: foreign key to learning resource
        status: current status: not_started, in_progress, completed
        """

        return cls(
            learning_resource_id=learning_resource_id,
            status=status 
        )