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
    """
    Represents a content object in the database.

    Attributes:
        pk (int): The primary key of the content.
        id (int): The unique identifier of the content.
        title (str): The title of the content.
        summary (str): The summary of the content.
        content (str): The full content.
        timestamp (str): The timestamp of when the content was created.
        tags (list): The list of tags associated with the content.
        types (list): The list of types associated with the content.
    """

    __tablename__ = "contents"
    pk = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id = Column(Integer, nullable=False, unique=True)
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
    """
    Represents a tag in the database.
    """
    __tablename__ = "tags"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(512), nullable=True)

    contents = relationship(
        "Content",
        secondary=tags_association,
        back_populates="tags",
    )


class Type(BASE):
    """
    Represents a type in the database.
    """

    __tablename__ = "types"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(512), nullable=True)

    contents = relationship(
        "Content",
        secondary=types_association,
        back_populates="types",
    )
