from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

class Base(DeclarativeBase):
    pass

class LearningPath(Base):
    """
    Main container for a learning journey
    Examples:
    -"Machine Learning Fundamentals"
    -"AWS Solutions Architect Prep"

    A learning path contains multiple modules which in turn contains resources
    """

    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    goal: Mapped[Optional[str]]  = mapped_column(Text, nullable=True)
    estimated_duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
    # modules: Mapped[List["Module"]] = relationship(
    #     back_populates="learning_path",
    #     cascade="all, delete-orphan",
    #     lazy="dynamic",
    #     order_by="Module.order_index"
    # )

    def __repr__(self):
        return f"<LearningPath(id={self.id}, name={self.name}, active={self.is_active})>"

    def __str__(self):
        return self.name

    #helper methods

    @property
    def module_count(self):
        """Get the total number of modules in learning path"""
        #Complete after module model finish
        return 0

    @property
    def total_resources(self):
        """Get the total number of resources across all modules"""
        #Complete after resource model finish
        return 0 

    @property
    def percent_complete(self):
        """
        Calculate percent complete based on completed resources
        Returns float between 0 and 100
        """
        #Complete after resource model finish
        return 0

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'goal': self.goal,
            'estimated_duration_days': self.estimated_duration_days,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'module_count': self.module_count,
        }

    @classmethod
    def create(cls, name, description=None, goal=None, estimated_duration_days=None):
        """
        Factory method to create a new learning path.
        
        Args:
            name (str): The name of the learning path
            description (str, optional): Detailed description
            goal (str, optional): Learning objectives
            estimated_duration_days (int, optional): Expected completion time
            
        Returns:
            LearningPath: A new LearningPath instance
        """
        return cls(
            name=name,
            description=description,
            goal=goal,
            estimated_duration_days=estimated_duration_days,
            is_active=True
        )

    def archive(self):
        """Archive this learning path (soft delete)"""
        self.is_active = False
    
    def update_info(self, name=None, description=None, goal=None, estimated_duration_days=None):
        """
        Update learning path information.
        
        Args:
            name (str, optional): New name
            description (str, optional): New description
            goal (str, optional): New learning goals
            estimated_duration_days (int, optional): New duration estimate
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if goal is not None:
            self.goal = goal
        if estimated_duration_days is not None:
            self.estimated_duration_days = estimated_duration_days