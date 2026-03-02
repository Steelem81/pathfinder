from datetime import datetime
from .base import Base
from typing import Optional
from sqlalchemy import ForeignKey, func, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

class QuizQuestion(Base):

    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    learning_resource_id: Mapped[int] = mapped_column(ForeignKey("learning_resources.id", ondelete="CASCADE"), index=True)
    question_type: Mapped[str]
    question_text: Mapped[str]
    correct_answer: Mapped[str] 
    options_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    explanation: Mapped[str]
    difficulty: Mapped[str]
    concept_tested: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    learning_resource: Mapped["LearningResource"] = relationship(back_populates="quiz_questions")

    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship(
        "QuizAttempt",
        back_populates="quiz_question",
        cascade="all, delete-orphan",
        order_by="QuizAttempt.attempted_at"
    )

    @classmethod
    def create(
        cls,
        learning_resource_id: int,
        question_type: str,
        question_text: str,
        correct_answer: str,
        explanation: str,
        difficulty: str,
        concept_tested: str,
        options_json: Optional[dict] = None
    ) -> "QuizQuestion": 
        """
        Create a quiz question for a given learning resource
        """
        return cls(
            learning_resource_id=learning_resource_id,
            question_type=question_type,
            question_text=question_text,
            correct_answer=correct_answer,
            explanation=explanation,
            difficulty=difficulty,
            concept_tested=concept_tested,
            options_json=options_json
        )

    