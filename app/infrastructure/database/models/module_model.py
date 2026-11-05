from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class ModuleModel(Base):
    __tablename__ = "modules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    position: Mapped[int] = mapped_column(Integer)

    course = relationship("CourseModel", back_populates="modules")
    sections = relationship(
        "SectionModel",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="SectionModel.position",
    )
