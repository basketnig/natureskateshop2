import sqlalchemy

from db_session import SqlAlchemyBase


class Things(SqlAlchemyBase):
    __tablename__ = 'clothes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Numeric)
    imgurl = sqlalchemy.Column(sqlalchemy.String)
    color = sqlalchemy.Column(sqlalchemy.String)
    size = sqlalchemy.Column(sqlalchemy.String)
    availbility = sqlalchemy.Column(sqlalchemy.Boolean, default=False)