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
    BooleanProperty,
    UniqueIdProperty
)


class ContactRel(StructuredRel):
    date = DateProperty(
        default=lambda: datetime.datetime.now()
    )
    location = StringProperty()


class Person(StructuredNode):
    uid = UniqueIdProperty()
    mobile_phone = StringProperty()
    verified = BooleanProperty()
    infected = BooleanProperty()
    incubation_start_date = DateProperty()

    contacted_persons = RelationshipTo('Person', 'HAS_TOUCHED', model=ContactRel)
