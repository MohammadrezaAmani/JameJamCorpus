from package_name import get_session
from package_name.db import (
    async_create_content,
    async_type_association,
    async_tag_association,
    async_create_tag,
    async_create_type,
)


async def add_to_db(data: dict):
    session = get_session()
    session = next(session)
    data["timestamp"] = str(data["timestamp"])
    content_id = await async_create_content(session=session, **data)
    for tag in data["tags"]:
        tag_id = await async_create_tag(session=session, name=tag)
        await async_tag_association(
            session=session, content_id=content_id.id, tag_id=tag_id.id
        )
    for typ in data["types"]:
        type_id = await async_create_type(session=session, name=typ)
        await async_type_association(
            session=session, content_id=content_id.id, type_id=type_id.id
        )
    print("\r", data["id"], end=" ")
