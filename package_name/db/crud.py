from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from package_name.db.tables import create_tables
from package_name.db.tables import Tag, Type, Content
from package_name.db.tables import tags_association, types_association


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


async def main():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine("sqlite+aiosqlite:///data.db", echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(create_tables)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        await async_create_content(session, "summary1", "content1", [1, 2], [1, 2])
        await async_create_content(session, "summary2", "content2", [2, 3], [2, 3])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
