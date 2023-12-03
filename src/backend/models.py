import uuid

from sqlalchemy import Column, Boolean, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, JSON

from database import Base


class MLModel(Base):
    __tablename__ = 'ml_models'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    model_name = Column(String, nullable=False)
    model_parameters = Column(JSON, nullable=False)
    is_trained = Column(Boolean, nullable=False, default=False)
    model_serialized = Column(LargeBinary, nullable=True)
    target_name = Column(String, nullable=True)
    train_dataset_file_path = Column(String, nullable=True)
    val_dataset_file_path = Column(String, nullable=True)
    train_loss = Column(LargeBinary, nullable=True)
    val_loss = Column(LargeBinary, nullable=True)
