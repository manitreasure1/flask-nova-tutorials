from sqlalchemy import String,  Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] 
    approved: Mapped[bool] = mapped_column(default=False)
