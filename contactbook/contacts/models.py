from django.db import models

from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)


class Person(StructuredNode):
    first_name = StringProperty()
    last_name = StringProperty()
    mobile_phone = StringProperty()
    email = StringProperty()

    contacted_persons = RelationshipTo('Person', 'HAS_TOUCHED')
