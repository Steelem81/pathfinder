from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class Module(Base):
    """
    Topics Units within a learning path
    

    A module contains multiple resources
    A learning path contains multiple modules
    """

    __tablename__ = "modules"

    id = Mapped[int] = mapped_column(primary_key=True)
    learning_path_id = Mapped[int] = mapped_column(ForeignKey("learning_path.id"), index=True)
    name = Mapped[str]
    description = Mapped[Optional[str]]
    order_index = Mapped[int] = mapped_column(index=True)
    duration_days = Mapped[Optional[int]]
    prereqs_json = Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    learning_objectives = Mapped[Optional[str]]
    created_at = Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at = Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Module(id={self.id}, name={self.name})>"

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, learning_path, order_index, description=None, duration_days=None, prereqs_json=None, learning_objectives=None):
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
            
        Returns:
            Module: A new Module instance
        """
        return cls(
            name=name,
            learning_path=learning_path,
            order_index=order_index,
            description=description,
            duration_days=duration_days,
            prereqs_json=prereqs_json,
            learning_objectives=learning_objectives
        )

    def update_info(self, name=None, learning_path=None, order_index=None, description=None, duration_days=None, prereqs_json=None, learning_objectives=None):
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