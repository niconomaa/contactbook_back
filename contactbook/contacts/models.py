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
    date = DateProperty()
    location = StringProperty()


class Person(StructuredNode):
    uid = UniqueIdProperty()
    mobile_phone = StringProperty(unique_index=True)
    verified = BooleanProperty()
    infected = BooleanProperty()
    incubation_start_date = DateProperty()

    contacted_persons = Relationship('Person', 'HAS_TOUCHED', model=ContactRel)

    def get_contacted_persons(self, person):



        return