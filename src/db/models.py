from sqlalchemy import BigInteger, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    sources = relationship("UserSource", back_populates="user")

    def __str__(self):
        return self.id


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)

    last_modified = Column(
        DateTime, comment="Время последнего изменения веб-страницы")
    etag = Column(String(length=128), comment="Etag страницы")

    users = relationship("UserSource", back_populates="source")

    updated_at = Column(DateTime, comment="Время обновления")

    def __str__(self):
        return self.url


class UserSource(Base):
    __tablename__ = 'user_sources'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    source_id = Column(Integer, ForeignKey('sources.id'))

    user = relationship("User", back_populates="sources")
    source = relationship("Source", back_populates="users")

    created_at = Column(DateTime, comment="Время создания")
    updated_at = Column(DateTime, comment="Время обновления")
