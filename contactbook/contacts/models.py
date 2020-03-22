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
    verified = BooleanProperty(required=True)
    infected = BooleanProperty(required=True)
    incubation_start_date = DateTimeProperty(required=False)

    contacted_persons = Relationship('Person', 'HAS_TOUCHED', model=ContactRel)

    def get_contacted_persons_after_infection(self):
        """ WIP: Traverse along relationships of self in order to get all possibly infected contact persons.

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