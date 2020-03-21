from django.db import models
import datetime

from neomodel import (
    StringProperty,
    StructuredNode,
    StructuredRel,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    DateProperty,
    BooleanProperty
)


class ContactRel(StructuredRel):
    date = DateProperty(
        default=lambda: datetime.datetime.now()
    )
    location = StringProperty()


class Person(StructuredNode):
    mobile_phone = StringProperty()
    verified = BooleanProperty()
    infected = BooleanProperty()

    contacted_persons = RelationshipTo('Person', 'HAS_TOUCHED', model=ContactRel)
