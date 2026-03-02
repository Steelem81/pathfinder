from .base import Base
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class QuizAttempt(Base):

    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("quiz_questions.id", ondelete="CASCADE"), index=True)
    user_answer: Mapped[str]
    is_correct: Mapped[bool]
    attempted_at: Mapped[datetime] = mapped_column(insert_default=func.now(), index=True)
    time_taken_secs: Mapped[int]
    confidence_level: Mapped[float]
    next_review_date: Mapped[datetime]
    repetition_count: Mapped[int]
    ease_factor: Mapped[str]
    interval_days: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())

    quiz_question: Mapped["QuizQuestion"] = relationship(back_populates="quiz_attempts")

    @classmethod
    def create(
        cls,
        question_id: int,
        attempted_at: datetime,
        time_taken_secs: int,
        confidence_level: float,
        next_review_date: datetime,
        repetition_count: int,
        ease_factor: str,
        interval_days: int
        ) -> "QuizAttempt":
            """
            Record quiz attempt

            """
            return cls(
                question_id=question_id,
                attempted_at=attempted_at,
                time_taken_secs=time_taken_secs,
                confidence_level=confidence_level,
                next_review_date=next_review_date,
                repetition_count=repetition_count,
                ease_factor=ease_factor,
                interval_days=interval_days
            )