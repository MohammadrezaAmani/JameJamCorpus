from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from package_name.db.tables import create_tables
from package_name.db.tables import Tag, Type, Content


async def create_content(
    session: AsyncSession,
    summary: str,
    content: str,
    tag_ids: list = None,
    type_ids: list = None,
):
    content_obj = Content(summary=summary, content=content)

    if tag_ids:
        tags = await session.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
        content_obj.tags.extend(tags.scalars().all())

    if type_ids:
        types = await session.execute(select(Type).filter(Type.id.in_(type_ids)))
        content_obj.types.extend(types.scalars().all())

    session.add(content_obj)
    await session.commit()
    return content_obj


async def get_content(session: AsyncSession, content_id: int):
    result = await session.execute(select(Content).filter(Content.id == content_id))
    return result.scalar()


async def update_content(
    session: AsyncSession,
    content_id: int,
    summary: str = None,
    content: str = None,
    tag_ids: list = None,
    type_ids: list = None,
):
    content_obj = await get_content(session, content_id)

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


async def delete_content(session: AsyncSession, content_id: int):
    content_obj = await get_content(session, content_id)

    if content_obj:
        session.delete(content_obj)
        await session.commit()
        return True
    return False


async def create_tag(session: AsyncSession, name: str):
    tag_obj = Tag(name=name)
    session.add(tag_obj)
    await session.commit()
    return tag_obj


async def get_tag(session: AsyncSession, tag_id: int):
    result = await session.execute(select(Tag).filter(Tag.id == tag_id))
    return result.scalar()


async def update_tag(session: AsyncSession, tag_id: int, name: str):
    tag_obj = await get_tag(session, tag_id)

    if tag_obj:
        tag_obj.name = name
        await session.commit()
        return tag_obj
    return None


async def delete_tag(session: AsyncSession, tag_id: int):
    tag_obj = await get_tag(session, tag_id)

    if tag_obj:
        session.delete(tag_obj)
        await session.commit()
        return True
    return False


async def create_type(session: AsyncSession, name: str):
    type_obj = Type(name=name)
    session.add(type_obj)
    await session.commit()
    return type_obj


async def get_type(session: AsyncSession, type_id: int):
    result = await session.execute(select(Type).filter(Type.id == type_id))
    return result.scalar()


async def update_type(session: AsyncSession, type_id: int, name: str):
    type_obj = await get_type(session, type_id)

    if type_obj:
        type_obj.name = name
        await session.commit()
        return type_obj
    return None


async def delete_type(session: AsyncSession, type_id: int):
    type_obj = await get_type(session, type_id)

    if type_obj:
        session.delete(type_obj)
        await session.commit()
        return True
    return False


async def main():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine("sqlite+aiosqlite:///data.db", echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(create_tables)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        await create_content(session, "summary1", "content1", [1, 2], [1, 2])
        await create_content(session, "summary2", "content2", [2, 3], [2, 3])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
