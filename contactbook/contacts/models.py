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


# class ContactEvent(models.Model):
#     contact_A = models.ForeignKey(Contact, on_delete=models.CASCADE)
#     contact_B = models.ForeignKey(Contact, on_delete=models.CASCADE)
#     date = models.DateField()
