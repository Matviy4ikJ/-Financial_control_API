from datetime import datetime

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()

    transactions = relationship('Transaction', back_populates='user', cascade='all, delete-orphan')
    categories = relationship('Category', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('Goal', back_populates='user', cascade='all, delete-orphan')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    note: Mapped = mapped_column(String(250), nullable=True)

    user = relationship('User', back_populates='transactions')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user = relationship('User', back_populates='categories')


class Goal(Base):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_amount: Mapped[int] = mapped_column(nullable=False)
    current_amount: Mapped[int] = mapped_column(default=0.0)
    deadline: Mapped[datetime] = mapped_column(nullable=False)

    user = relationship('User', back_populates='goals')
