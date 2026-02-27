from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Boolean, func, UniqueConstraint
from datetime import datetime, date
from typing import Optional

class Schedule(Base):
    """
    Schedules for when resources are delivered

    """

    __tablename__= 'schedules'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    learning_resource_id: Mapped[int] = mapped_column(ForeignKey("learning_resources.id", ondelete="CASCADE"), index=True)
    scheduled_date: Mapped[datetime] = mapped_column(index=True)
    delivered: Mapped[bool] = mapped_column(default=False)
    delivered_at: Mapped[Optional[datetime]]
    notification_sent: Mapped[Optional[bool]]
    notification_sent_at: Mapped[Optional[datetime]]
    reschedule_count: Mapped[int] = mapped_column(default=0)
    original_scheduled_date: Mapped[Optional[datetime]]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    learning_resource: Mapped["LearningResource"] = relationship(back_populates= "schedules")

    __table_args__ = (
        UniqueConstraint('learning_resource_id', 'scheduled_date', name='uq_resource_date'),
    )

    @property
    def is_overdue(self) -> bool:
        today = date.today()
        return self.scheduled_date < today and not self.delivered
    
    @property
    def is_today(self) -> bool:
        return self.scheduled_date == date.today()

    # Helper Functions


    @classmethod
    def create(
        cls,
        learning_resource_id: int,
        scheduled_date: datetime,
        scheduled_time: str="07:00"
    ) -> "Schedule":
        """
        Creates a schedule for a learning resource

        Args:
            learning_resource_id: Foreign key to learning resource
            scheduled_date: When the resource is scheduled to be delivered
            scheduled_time: time of day the resources is scheduled to be delivered
        """
        return cls(
            learning_resource_id=learning_resource_id,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time
        )
    
    def mark_delivered(self):
        self.delivered = True
        self.delivered_at = datetime.utcnow()

    def reschedule(self):
        """TODO - create ability to reschedule"""
        pass
    