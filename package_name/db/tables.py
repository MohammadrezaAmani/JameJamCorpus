from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)

from sqlalchemy.orm import declarative_base, relationship


BASE = declarative_base()

tags_association = Table(
    "tags_association",
    BASE.metadata,
    Column("content_id", Integer, ForeignKey("contents.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

types_association = Table(
    "types_association",
    BASE.metadata,
    Column("content_id", Integer, ForeignKey("contents.id")),
    Column("type_id", Integer, ForeignKey("types.id")),
)


class Content(BASE):
    __tablename__ = "contents"
    pk = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    title = Column(String(512), nullable=True)
    summary = Column(String(512), nullable=True)
    content = Column(Text, nullable=True)
    timestamp = Column(String(512), nullable=True)
    tags = relationship(
        "Tag",
        secondary=tags_association,
        back_populates="contents",
        order_by="Tag.id",
    )

    types = relationship(
        "Type",
        secondary=types_association,
        back_populates="contents",
        order_by="Type.id",
    )

    def __init__(self, id, title, summary, content, timestamp):
        self.id = id
        self.summary = summary
        self.content = content
        self.title = title
        self.timestamp = timestamp

    def __repr__(self):
        return (
            f"Content(id={self.id}, summary={self.summary!r}, content={self.content!r})"
        )


class Tag(BASE):
    __tablename__ = "tags"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(512), nullable=True)

    contents = relationship(
        "Content",
        secondary=tags_association,
        back_populates="tags",
    )


class Type(BASE):
    __tablename__ = "types"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(512), nullable=True)

    contents = relationship(
        "Content",
        secondary=types_association,
        back_populates="types",
    )


def create_tables(engine):
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine, checkfirst=True)
