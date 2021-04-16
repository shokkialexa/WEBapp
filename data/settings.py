import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Settings(SqlAlchemyBase):
    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='dark')
    cards_in_hand = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=6)
    cards_in_deck = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=30)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')