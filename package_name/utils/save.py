
# from package_name.db import (
#     async_create_content,
#     async_type_association,
#     async_tag_association,
#     async_create_tag,
#     async_create_type,
#     async_tag_association,
#     async_type_association,
# )
from package_name.db.crud2 import (
    add_content,
    add_tag,
    add_type,
    add_tag_association,
    add_type_association,
)


async def add_to_db(data: dict):
    data["timestamp"] = str(data["timestamp"])
    content_id = add_content(data)
    for tag in data["tags"]:
        tag_id = add_tag(tag)
        add_tag_association(content_id.id, tag_id.id)
    for typ in data["types"]:
        type_id = add_type(typ)
        add_type_association(content_id.id, type_id.id)
