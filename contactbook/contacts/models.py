from django.db import models

from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship
)


class Contact(StructuredNode):
    first_name = StringProperty()
    last_name = StringProperty()
    mobile_phone = StringProperty()
    email = StringProperty()

    contacts = RelationshipTo('Contact', 'HAS_TOUCHED')