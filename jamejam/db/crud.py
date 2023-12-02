from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, desc, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from jamejam import config
from jamejam.db.tables import Tag, Type, Content
from jamejam.db.tables import tags_association, types_association


async def async_create_content(
    session: AsyncSession,
    id: int,
    title: str,
    summary: str,
    content: str,
    timestamp: int,
    tags: list = None,
    types: list = None,
):
    content_obj = Content(
        id=id, summary=summary, content=content, timestamp=timestamp, title=title
    )
    session.add(content_obj)
    await session.commit()
    return content_obj


async def async_get_content(session: AsyncSession, content_id: int):
    result = await session.execute(select(Content).filter(Content.id == content_id))
    return result.scalar()


async def async_update_content(
    session: AsyncSession,
    content_id: int,
    summary: str = None,
    content: str = None,
    tag_ids: list = None,
    type_ids: list = None,
):
    content_obj = await async_get_content(session, content_id)

    if content_obj:
        if summary:
            content_obj.summary = summary
        if content:
            content_obj.content = content

        if tag_ids:
            tags = await session.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
            content_obj.tags = tags.scalars().all()

        if type_ids:
            types = await session.execute(select(Type).filter(Type.id.in_(type_ids)))
            content_obj.types = types.scalars().all()

        await session.commit()
        return content_obj
    return None


async def async_delete_content(session: AsyncSession, content_id: int):
    content_obj = await async_get_content(session, content_id)

    if content_obj:
        session.delete(content_obj)
        await session.commit()
        return True
    return False


async def async_create_tag(session: AsyncSession, name: str):
    result = await session.execute(select(Tag).filter(Tag.name == name))
    tag_obj = result.scalar()
    if tag_obj:
        return tag_obj
    tag_obj = Tag(name=name)
    session.add(tag_obj)
    await session.commit()
    return tag_obj


async def async_get_tag(session: AsyncSession, tag_id: int):
    result = await session.execute(select(Tag).filter(Tag.id == tag_id))
    return result.scalar()


async def async_update_tag(session: AsyncSession, tag_id: int, name: str):
    tag_obj = await async_get_tag(session, tag_id)

    if tag_obj:
        tag_obj.name = name
        await session.commit()
        return tag_obj
    return None


async def async_delete_tag(session: AsyncSession, tag_id: int):
    tag_obj = await async_get_tag(session, tag_id)

    if tag_obj:
        session.delete(tag_obj)
        await session.commit()
        return True
    return False


async def async_create_type(session, name: str):
    result = await session.execute(select(Type).filter(Type.name == name))
    type_obj = result.scalar()
    if type_obj:
        return type_obj
    type_obj = Type(name=name)
    session.add(type_obj)
    await session.commit()
    return type_obj


async def async_get_type(session: AsyncSession, type_id: int):
    result = await session.execute(select(Type).filter(Type.id == type_id))
    return result.scalar()


async def async_update_type(session: AsyncSession, type_id: int, name: str):
    type_obj = await async_get_type(session, type_id)

    if type_obj:
        type_obj.name = name
        await session.commit()
        return type_obj
    return None


async def async_delete_type(session: AsyncSession, type_id: int):
    type_obj = await async_get_type(session, type_id)

    if type_obj:
        session.delete(type_obj)
        await session.commit()
        return True
    return False


async def async_tag_association(session: AsyncSession, content_id: int, tag_id: int):
    await session.execute(
        tags_association.insert().values(content_id=content_id, tag_id=tag_id)
    )
    await session.commit()


async def async_type_association(session: AsyncSession, content_id: int, type_id: int):
    await session.execute(
        types_association.insert().values(content_id=content_id, type_id=type_id)
    )
    await session.commit()


def create_content(
    session: Session,
    summary: str,
    content: str,
    tag_ids: list = None,
    type_ids: list = None,
):
    content_obj = Content(summary=summary, content=content)

    if tag_ids:
        tags = session.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
        content_obj.tags.extend(tags.scalars().all())

    if type_ids:
        types = session.execute(select(Type).filter(Type.id.in_(type_ids)))
        content_obj.types.extend(types.scalars().all())

    session.add(content_obj)
    session.commit()
    return content_obj


def get_content(session: Session, content_id: int):
    result = session.execute(select(Content).filter(Content.id == content_id))
    return result.scalar()


def update_content(
    session: Session,
    content_id: int,
    summary: str = None,
    content: str = None,
    tag_ids: list = None,
    type_ids: list = None,
):
    content_obj = get_content(session, content_id)

    if content_obj:
        if summary:
            content_obj.summary = summary
        if content:
            content_obj.content = content

        if tag_ids:
            tags = session.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
            content_obj.tags = tags.scalars().all()

        if type_ids:
            types = session.execute(select(Type).filter(Type.id.in_(type_ids)))
            content_obj.types = types.scalars().all()

        session.commit()
        return content_obj
    return None


def delete_content(session: Session, content_id: int):
    content_obj = get_content(session, content_id)

    if content_obj:
        session.delete(content_obj)
        session.commit()
        return True
    return False


def create_tag(session: Session, name: str):
    tag_obj = Tag(name=name)
    session.add(tag_obj)
    session.commit()
    return tag_obj


def get_tag(session: Session, tag_id: int):
    result = session.execute(select(Tag).filter(Tag.id == tag_id))
    return result.scalar()


def update_tag(session: Session, tag_id: int, name: str):
    tag_obj = get_tag(session, tag_id)

    if tag_obj:
        tag_obj.name = name
        session.commit()
        return tag_obj
    return None


def delete_tag(session: Session, tag_id: int):
    tag_obj = get_tag(session, tag_id)

    if tag_obj:
        session.delete(tag_obj)
        session.commit()
        return True
    return False


def create_type(session: Session, name: str):
    type_obj = Type(name=name)
    session.add(type_obj)
    session.commit()
    return type_obj


def get_type(session: Session, type_id: int):
    result = session.execute(select(Type).filter(Type.id == type_id))
    return result.scalar()


async def get_types(session: Session):
    result = await session.execute(select(Type))
    return result.scalars().all()


async def get_tags(session: Session):
    result = await session.execute(select(Tag))
    return result.scalars().all()


async def get_contents(
    session: Session,
    start: int = 0,
    end: int = None,
    sort_by: str = "id",
    sort_order: str = "asc",
):
    result = await session.execute(
        select(Content)
        .order_by(
            asc(getattr(Content, sort_by))
            if sort_order == "asc"
            else desc(getattr(Content, sort_by))
        )
        .offset(start)
        .limit(end)
    )
    for row in result:
        yield row


async def get_tags_by_content(session: Session, content_id: int):
    result = await session.execute(
        select(Tag)
        .join(tags_association)
        .filter(tags_association.c.content_id == content_id)
    )
    return result.scalars().all()


async def get_types_by_content(session: Session, content_id: int):
    result = await session.execute(
        select(Type)
        .join(types_association)
        .filter(types_association.c.content_id == content_id)
    )
    return result.scalars().all()


def update_type(session: Session, type_id: int, name: str):
    type_obj = get_type(session, type_id)

    if type_obj:
        type_obj.name = name
        session.commit()
        return type_obj
    return None


def delete_type(session: Session, type_id: int):
    type_obj = get_type(session, type_id)

    if type_obj:
        session.delete(type_obj)
        session.commit()
        return True
    return False


def tag_association(session: Session, content_id: int, tag_id: int):
    session.execute(
        tags_association.insert().values(content_id=content_id, tag_id=tag_id)
    )
    session.commit()


def type_association(session: Session, content_id: int, type_id: int):
    session.execute(
        types_association.insert().values(content_id=content_id, type_id=type_id)
    )
    session.commit()


def remove_duplicates():
    def get_items(session, model):
        result = session.execute(select(model).order_by(getattr(model, "id").desc()))
        return result.scalars().all()

    database_url = config.DATABASE_URL.replace("+asyncpg", "+psycopg2")
    database_url = database_url.replace("+aiosqlite", "")
    engine = create_engine(database_url)

    Session = sessionmaker(bind=engine)
    session = Session()

    def solve_duplicates(session):
        handle_duplicates(session, Tag, tags_association, "tag_id")
        handle_duplicates(session, Type, types_association, "type_id")

    def handle_duplicates(session, model, association_table, column_name):
        items = get_items(session, model)
        for item in items:
            result = session.execute(
                select(model)
                .filter(getattr(model, "name") == item.name)
                .order_by(getattr(model, "id").desc())
            )
            data = list(result.scalars().all())
            if len(data) > 1:
                for item in data[1:]:
                    session.execute(
                        association_table.update()
                        .where(getattr(association_table.c, column_name) == item.id)
                        .values({column_name: data[0].id})
                    )
                for item in data[1:]:
                    session.delete(item)
                session.commit()

                session.commit()
            else:
                ...

    solve_duplicates(session)
    session.close()
