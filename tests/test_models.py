from shisanjing.models.base import Annotation, EntityRef, Token


def test_annotation_defaults():
    ann = Annotation(book="lunyu", text="子曰")
    assert ann.chapter is None
    assert ann.entities == []
    assert ann.tokens == []


def test_entity_ref():
    e = EntityRef(name="孔子", entity_type="person", start=0, end=2)
    assert e.name == "孔子"
    assert e.entity_type == "person"


def test_token():
    t = Token(text="子", pos="n")
    assert t.text == "子"
