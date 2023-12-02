import logging
from package_name import get_session
from package_name.config import DEBUG, START, END
from package_name.db import (
    async_create_content,
    async_type_association,
    async_tag_association,
    async_create_tag,
    async_create_type,
)
from package_name.db.crud import (
    get_contents,
    get_tags,
    get_types,
    get_tags_by_content,
    get_types_by_content,
)

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)


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
    if DEBUG:
        logging.debug(f"Data added to database from {data['id']}")
    await session.close()


async def to_file(
    file_path: str,
    sep: str = ",",
    header: bool = True,
    encoding: str = "utf-8",
    sort_by: str = "id",
    sort_order: str = "asc",
    start: int = START,
    end: int = END,
    mode: str = "w",
    include_tags: bool = True,
    include_types: bool = True,
    end_char: str = "\n",
):
    session = get_session()
    session = next(session)

    if DEBUG:
        logging.debug("writing to file")
    with open(file_path, mode=mode, encoding=encoding) as f:
        contents = get_contents(
            session=session,
            start=start,
            end=end,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        if include_tags:
            tags = await get_tags(session=session)
            tags = list(map(lambda i: i.name, tags))
        if include_types:
            types = await get_types(session=session)
            types = list(map(lambda i: i.name, types))

        if header:
            if include_tags and include_types:
                f.write(
                    f"id{sep}title{sep}summary{sep}content{sep}timestamp{sep}{sep.join(tags)}{sep}{sep.join(types)}{end_char}"
                )
            elif include_tags:
                f.write(
                    f"id{sep}title{sep}summary{sep}content{sep}timestamp{sep}{sep.join(tags)}{end_char}"
                )
            elif include_types:
                f.write(
                    f"id{sep}title{sep}summary{sep}content{sep}timestamp{sep}{sep.join(types)}{end_char}"
                )
            else:
                f.write(f"id{sep}title{sep}summary{sep}content{sep}timestamp{end_char}")
        async for content in contents:
            content = content[0]

            content_tags = await get_tags_by_content(
                session=session, content_id=content.id
            )
            content_tags = list(map(lambda i: i.name, content_tags))
            content_types = await get_types_by_content(
                session=session, content_id=content.id
            )
            content_types = list(map(lambda i: i.name, content_types))
            if include_tags and include_types:
                content_tags = list(
                    map(lambda i: "1" if i in content_tags else "0", tags)
                )
                content_types = list(
                    map(lambda i: "1" if i in content_types else "0", types)
                )
                c = content.content.replace("\n", "", content.content.count("\n"))
                f.write(
                    f"{content.id}{sep}{content.title}{sep}{content.summary}{sep}{c}{sep}{content.timestamp}{sep}{sep.join(content_tags)}{sep}{sep.join(content_types)}{end_char}"
                )
            elif include_tags:
                content_tags = list(
                    map(lambda i: "1" if i in content_tags else "0", tags)
                )
                f.write(
                    f"{content.id}{sep}{content.title}{sep}{content.summary}{sep}{content.content}{sep}{content.timestamp}{sep}{sep.join(content_tags)}{end_char}"
                )
            elif include_types:
                content_types = list(
                    map(lambda i: "1" if i in content_types else "0", types)
                )
                f.write(
                    f"{content.id}{sep}{content.title}{sep}{content.summary}{sep}{content.content}{sep}{content.timestamp}{sep}{sep.join(content_types)}{end_char}"
                )
            else:
                f.write(
                    f"{content.id}{sep}{content.title}{sep}{content.summary}{sep}{content.content}{sep}{content.timestamp}{end_char}"
                )
    await session.close()
