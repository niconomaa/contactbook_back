import graphene
import datetime
from django.utils import timezone
from contacts.models import Person

'''
NOTE:   It is not possible to use 'DjangoObjectType' with Neomodels since they do not inherit from Django base models.
        For this reason we have to use the basic 'ObjectType' for Neomodels here. 
'''


class PersonType(graphene.ObjectType):
    uid = graphene.String()
    mobile_phone = graphene.String()
    danger = graphene.String()
    verified = graphene.Boolean()
    infected = graphene.Boolean()
    incubation_start_date = graphene.DateTime()


class AddPerson(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        mobile_phone = graphene.String(required=True)

    def mutate(self, info, mobile_phone):
        person = Person.nodes.get_or_none(mobile_phone=mobile_phone)

        if person is None:
            # Person does not exist as node yet
            person = Person(
                mobile_phone=mobile_phone,
                verified=True,
                infected=False,
                incubation_start_date=None
            )
            person.save()
        elif not person.verified:
            # Person already exists as node and is to be verified
            person.verified = True
            person.save()

        return AddPerson(person=person)


class MarkMeAsInfected(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        uid = graphene.String(required=True)

    def mutate(self, info, uid):
        person = Person.nodes.get(uid=uid)
        person.infected = True
        person.incubation_start_date = datetime.datetime.now()
        person.save()

        return MarkMeAsInfected(person=person)


class MarkMeAsNotInfected(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        uid = graphene.String(required=True)

    def mutate(self, info, uid):
        person = Person.nodes.get(uid=uid)
        person.infected = False
        person.incubation_start_date = None
        person.save()

        return MarkMeAsNotInfected(person=person)


class AddNewContactPerson(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        my_uid = graphene.String(required=True)
        contact_mobile_phone = graphene.String(required=True)

    def mutate(self, info, my_uid, contact_mobile_phone):

        # if the person hasn't yet registered, make new entry for number
        if Person.nodes.get_or_none(mobile_phone=contact_mobile_phone) is None:
            contact_person = Person(
                mobile_phone=contact_mobile_phone,
                verified=False,
                infected=False,
                incubation_start_date=None
            )
            contact_person.save()
        else:
            contact_person = Person.nodes.get(mobile_phone=contact_mobile_phone)

        person = Person.nodes.get(uid=my_uid)
        rel = person.contacted_persons.connect(contact_person)
        rel.date = datetime.datetime.now()
        rel.location = "Unknown"
        rel.save()

        return AddNewContactPerson(person=contact_person)


class HelperMethods:
    # see if the connection between two nodes is legit (my_node is tuple(node, last_connection_time))
    def is_valid_traversal(self, my_node, node):
        time_next_connection = my_node[0].contacted_persons.relationship(node).date
        return_val = False
        # only go back in time and no further than 30 days
        if my_node[1] > time_next_connection > (timezone.now() - datetime.timedelta(30)):
            return_val = True

        return return_val

    # return a list of tuples(node, last_connection_time) of adjacent valid nodes
    def make_adj_tuples(self, my_node, contacted):
        adj = []
        for node in contacted:
            if self.is_valid_traversal(my_node, node):
                adj.append((node, my_node[0].contacted_persons.relationship(node).date))

        return adj


class ShouldIBeWorried(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        uid = graphene.String(required=True)

    def mutate(self, info, uid):
        helper = HelperMethods()
        person = Person.nodes.get(uid=uid)
        now = timezone.now()
        next_layer = []
        my_node = (person, now)
        contacted = person.contacted_persons.all()
        adjacent = helper.make_adj_tuples(my_node, contacted)
        depth = 3
        incubation_healing_time = datetime.timedelta(14)

        for i in range(depth):
            for node in adjacent:
                if node[0].infected:
                    incubation_t = node[0].incubation_start_date
                    if (incubation_t - incubation_healing_time) < now < (incubation_t + incubation_healing_time):
                        person.danger = i
                        person.save()
                        return ShouldIBeWorried(person=person)

                new_connected = node[0].contacted_persons.all()
                new_adj = helper.make_adj_tuples(node, new_connected)
                for a in new_adj:
                    next_layer.append(a)

            adjacent = next_layer
            next_layer = []

        person.danger = 3
        person.save()
        return ShouldIBeWorried(person=person)


class Mutation(graphene.ObjectType):
    add_person = AddPerson.Field()
    mark_me_as_infected = MarkMeAsInfected.Field()
    mark_me_as_not_infected = MarkMeAsNotInfected.Field()
    add_new_contact_person = AddNewContactPerson.Field()
    should_i_be_worried = ShouldIBeWorried.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(
        PersonType,
        uid=graphene.String()
    )

    def resolve_me(self, info, uid):
        return Person.nodes.get(uid=uid)

    all_persons = graphene.List(
        PersonType
    )

    def resolve_all_persons(self, info, **kwargs):
        # Use 'Person.nodes' instead of 'Person.objects' here
        return Person.nodes.all()

    has_contact_today = graphene.Boolean(
        uid=graphene.String()
    )

    def resolve_has_contact_today(self, info, uid):
        person = Person.nodes.get(uid=uid)

        for contact_person in person.contacted_persons:
            rel = person.contacted_persons.relationship(contact_person)
            today = datetime.datetime.now()

            if today.day == rel.date.day:
                return True

        return False

    streak = graphene.Int(
        uid=graphene.String()
    )

    def resolve_streak(self, info, uid):
        person = Person.nodes.get(uid=uid)
        return person.get_streak()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)