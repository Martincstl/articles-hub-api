from typing import Generic, TypeVar
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)

class BaseRepository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get_by_id(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        return instance

    def add(self,instance:ModelT) -> ModelT:
        self.db.add(instance)
        return instance

    def delete(self, instance: ModelT) -> None:
        self.db.delete(instance)

    def flush(self) -> None:
        self.db.flush()