from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'
    items = relationship("Item", cascade="all, delete-orphan")
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
           'name': self.name,
           'id': self.id
               }


class Item(Base):
    __tablename__ = 'item'

    category = relationship("Category", backref=backref
                            ("items", cascade="all, delete-orphan"))
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    created = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    @property
    def serialize(self):
        return {
           'name': self.name,
           'description': self.description,
           'id': self.id
            }

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
