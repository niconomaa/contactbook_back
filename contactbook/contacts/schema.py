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
    verified = graphene.Boolean()
    infected = graphene.Boolean()
    incubation_start_date = graphene.Date()


class AddPerson(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        mobile_phone = graphene.String(required=True)

    def mutate(self, info, mobile_phone):

        # only make new entry if the number hasn't been added yet
        if Person.nodes.get_or_none(mobile_phone=mobile_phone) is None:
            person = Person(
                mobile_phone=mobile_phone,
                verified=False,
                infected=False
            )
            person.save()
        else:
            person = Person.nodes.get(mobile_phone=mobile_phone)
            person.verified=False
            person.infected=False
            person.save()

        return AddPerson(person=person)


class MarkMeAsInfected(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        uid = graphene.String(required=True)

    def mutate(self, info, uid):
        person = Person.nodes.get(uid=uid)

        person.infected = True
        person.save()

        return MarkMeAsInfected(person=person)


class AddNewContactPerson(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        my_uid = graphene.String(required=True)
        contact_mobile_phone = graphene.String(required=True)

    def mutate(self, info, my_uid, contact_mobile_phone):

        # if the person hasn't yet registered, make new entry for number
        if Person.nodes.get_or_none(mobile_phone=contact_mobile_phone) is None:
            contact_person = Person(
                mobile_phone=contact_mobile_phone
            )
            contact_person.save()
        else:
            contact_person = Person.nodes.get(mobile_phone=contact_mobile_phone)

        person = Person.nodes.get(uid=my_uid)
        rel = person.contacted_persons.connect(contact_person)
        rel.date = datetime.datetime.now()
        rel.location = "Unknown"
        rel.save()

        return AddNewContactPerson(person=person)


class Mutation(graphene.ObjectType):
    add_person = AddPerson.Field()
    mark_me_as_infected = MarkMeAsInfected.Field()
    add_new_contact_person = AddNewContactPerson.Field()


class Query(graphene.ObjectType):
    name = 'Query'
    description = '...'

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


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)