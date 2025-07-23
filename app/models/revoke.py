from app.extensions import db
from datetime import datetime
from sqlalchemy import String,  Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class RevokedToken(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


