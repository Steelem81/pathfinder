from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Integer, ForeignKey, JSON, func
from .base import Base

class LearningResource(Base):
    """
    Individual learning resources
    Examples:
    -Youtube tutorial videos
    -professional journal articles

    A module contains multiple learning resources
    """
    __tablename__= 'learning_resources'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    title: Mapped[str]
    order_index: Mapped[int] = mapped_column(index=True)
    resource_type: Mapped[str]
    url: Mapped[Optional[str]]
    file_path: Mapped[Optional[str]]
    content: Mapped[Optional[str]]
    summary: Mapped[Optional[str]]
    key_concepts: Mapped[Optional[str]] = mapped_column(JSON)
    difficulty: Mapped[Optional[str]]
    estimated_time_mins: Mapped[Optional[int]]
    source_metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    module = relationship("Module", back_populates="learning_resources")
    schedules: Mapped[List["Schedule"]] = relationship(
        "Schedule",
        back_populates="learning_resource", 
        cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Module(id={self.id}, title='{self.title}', order_index={self.order_index})>"
    
    def __str__(self) -> str:
        return self.title
    
    #Help Methods

    def to_dict(self) -> dict:
        """Convert model to dictionary for JSON seirlaization."""
        print("to be built at a later time")
        pass

    @classmethod
    def create(
        cls,
        module_id: int,
        order_index: int,
        title: str,
        resource_type: str = None,
        url: Optional[str] = None,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        key_concepts: Optional[JSON] = None,
        difficulty: Optional[str] = None,
        estimated_time_mins: Optional[str] = None,
        source_metadata_json: Optional[JSON] = None
    ) -> "LearningResource":
        """
        Factory method to create a new module.
        
        Args:
            module_id: Id of the parent module
            order_index: Position in the module sequence
            title: Referenceable title of the resource
            resource_type: Type of material
            url: source url if web-based
            file_path: Local file path if uploaded
            content: Extracted/processed content
            summary: LLM generated summary
            key_concepts: array of main concepts
            difficulty: beginner, intermediate, advanced
            estimated_time_mins: Estimated reading/viewing time
            source_metadata_json: author, publish date, etc...
            
        Returns:
            A new Resource instance
        """

        return cls(
            module_id=module_id,
            order_index=order_index,
            title=title,
            resource_type=resource_type,
            url=url,
            file_path=file_path,
            content=content,
            summary=summary,
            key_concepts=key_concepts,
            difficulty=difficulty,
            estimated_time_mins=destimated_time_mins,
            source_metadata_json=source_metadata_json
        )
    
    def update_learning_resource(
        self,
        order_index: Optional[int] = None,
        title: Optional[str] = None,
        resource_type: Optional[str] = None,
        url: Optional[str] = None,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        key_concepts: Optional[JSON] = None,
        difficulty: Optional[str] = None,
        estimated_time_mins: Optional[str] = None,
        source_metadata_json: Option[JSON] = None
    ) -> None:
        """ Update learning resource infomration"""
        if order_index is not None:
            self.order_index = order_index
        if title  is not None:
            self.title = title
        if resource_type is not None:
            self.resource_type = resource_type
        if url is not None:
            self.url=url
        if file_path is not None:
            self.file_path = file_path
        if content is not None:
            self.content = content
        if summary is not None:
            self.summary = summary
        if key_concepts is not None:
            self.key_concepts = key_concepts
        if difficulty is not None:
            self.difficulty = difficulty
        if estimated_time_mins is not None:
            self.estimated_time_mins = estimated_time_mins
        if source_metadata_json is not None:
            self.source_metadata_json = source_metadata_json

