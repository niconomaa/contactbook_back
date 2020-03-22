import graphene
import datetime
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


class ShouldIBeWorried(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        uid = graphene.String(required=True)

    def mutate(self, info, uid):
        person = Person.nodes.get(uid=uid)

        connected_infected = person.contacted_persons.search(infected=True)
        connected_healthy = person.contacted_persons.search(infected=False)
        sum_infected = len(connected_infected)
        sum_healthy = len(connected_healthy)

        connected_healthy_last = []

        if sum_infected > 0:
            danger = 1
        else:
            for node in connected_healthy:
                connected_infected_sec = node.contacted_persons.search(infected=True)
                connected_healthy_sec = node.contacted_persons.search(infected=False)
                connected_healthy_last.append(connected_healthy_sec)
                sum_infected += len(connected_infected_sec)
                sum_healthy += len(connected_healthy_sec)

            for node in [item for sublist in connected_healthy_last for item in sublist]:
                connected_infected_third = node.contacted_persons.search(infected=True)
                connected_healthy_third = node.contacted_persons.search(infected=False)
                sum_infected += len(connected_infected_third)
                sum_healthy += len(connected_healthy_third)

            if (sum_infected + sum_healthy) != 0:
                danger = sum_infected / (sum_infected + sum_healthy)
            else:
                danger = 0

        person.danger = danger
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


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)