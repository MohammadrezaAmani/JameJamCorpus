import threading
from package_name import SESSION
from .tables import Content, Tag, Type


DOCUMENT_INSERTION_LOCK = threading.RLock()


def add_content(data: dict):
    with DOCUMENT_INSERTION_LOCK:
        id = data["id"]
        title = data["title"]
        summary = data["summary"]
        content = data["content"]
        tags = data["tags"]
        types = data["types"]
        timestamp = data["timestamp"]

        content_obj = Content(
            id=id, title=title, summary=summary, content=content, timestamp=timestamp
        )
        SESSION.add(content_obj)
        SESSION.commit()
        SESSION.refresh(content_obj)

        for tag in tags:
            tag_obj = Tag(name=tag)
            SESSION.add(tag_obj)
            SESSION.commit()
            SESSION.refresh(tag_obj)
            content_obj.tags.append(tag_obj)

        for type in types:
            type_obj = Type(name=type)
            SESSION.add(type_obj)
            SESSION.commit()
            SESSION.refresh(type_obj)
            content_obj.types.append(type_obj)

        SESSION.commit()
        SESSION.refresh(content_obj)
        return content_obj


def add_tag(data: dict):
    with DOCUMENT_INSERTION_LOCK:
        name = data["name"]
        tag_obj = Tag(name=name)
        if SESSION.query(Tag).filter(Tag.name == name).first():
            return SESSION.query(Tag).filter(Tag.name == name).first()
        SESSION.add(tag_obj)
        SESSION.commit()
        SESSION.refresh(tag_obj)
        return tag_obj


def add_type(name: str):
    with DOCUMENT_INSERTION_LOCK:
        type_obj = Type(name=name)
        if SESSION.query(Type).filter(Type.name == name).first():
            return SESSION.query(Type).filter(Type.name == name).first()
        SESSION.add(type_obj)
        SESSION.commit()
        SESSION.refresh(type_obj)
        return type_obj


def add_type_association(content_id: int, type_id: int):
    with DOCUMENT_INSERTION_LOCK:
        content_obj = SESSION.query(Content).filter(Content.id == content_id).first()
        type_obj = SESSION.query(Type).filter(Type.id == type_id).first()
        if type_obj in content_obj.types:
            return content_obj
        content_obj.types.append(type_obj)
        SESSION.commit()
        SESSION.refresh(content_obj)
        return content_obj


def add_tag_association(content_id: int, tag_id: int):
    with DOCUMENT_INSERTION_LOCK:
        content_obj = SESSION.query(Content).filter(Content.id == content_id).first()
        tag_obj = SESSION.query(Tag).filter(Tag.id == tag_id).first()
        if tag_obj in content_obj.tags:
            return content_obj
        content_obj.tags.append(tag_obj)
        SESSION.commit()
        SESSION.refresh(content_obj)
        return content_obj
