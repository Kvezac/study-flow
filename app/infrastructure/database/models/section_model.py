from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class SectionModel(Base):
    __tablename__ = "sections"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, default="")
    position: Mapped[int] = mapped_column(Integer)

    module = relationship("ModuleModel", back_populates="sections")
    lectures = relationship(
        "LectureModel",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="LectureModel.position",
    )
