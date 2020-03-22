from django.db import models
import datetime
from neomodel.match import EITHER, Traversal

from neomodel import (
    StringProperty,
    StructuredNode,
    StructuredRel,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    DateTimeProperty,
    BooleanProperty,
    UniqueIdProperty
)


class ContactRel(StructuredRel):
    date = DateTimeProperty()
    location = StringProperty()


class Person(StructuredNode):
    uid = UniqueIdProperty()
    mobile_phone = StringProperty(unique_index=True)
    danger = StringProperty(default="0")
    verified = BooleanProperty(required=True)
    infected = BooleanProperty(required=True)
    incubation_start_date = DateTimeProperty(required=False)

    contacted_persons = Relationship('Person', 'HAS_TOUCHED', model=ContactRel)

    def get_contacted_persons(self):
        """ WIP: Traverse along relationships of self in order to get all contact persons.

        :return: set of nodes of type Person
        """
        assert self.infected

        definition = dict(
            node_class=Person,
            direction=EITHER,
            relation_type=None,
            model=ContactRel
        )
        relations_traversal = Traversal(self, Person.__label__, definition)
        # TODO: Implement condition correctly.
        # all_relations = relations_traversal.match(date__lt=datetime.datetime.now()).all()
        all_relations = relations_traversal.all()

        return all_relations

    def get_last_contact_date(self):
        """ Get last contact date among all contacts

        :return: [DateTime] last contact date
        """
        # TODO: Remove hardcoded value.
        last_contact_date = datetime.datetime.now() - datetime.timedelta(days=365)
        for contact_person in self.contacted_persons:
            for rel in self.contacted_persons.all_relationships(contact_person):
                contact_date = rel.date
                if contact_date.date() > last_contact_date.date():
                    last_contact_date = contact_date

        return last_contact_date

    def get_streak(self):
        """ Compute the streak, respectively the number of days the person did not have contact with another person.

        :return: [int] number of days to last_contact_date()
        """
        delta = datetime.datetime.now().date() - self.get_last_contact_date().date()
        return delta.days