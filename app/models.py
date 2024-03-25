from typing import Any, Dict

from sqlalchemy import Column, Integer, String

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    tags = Column(String)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
