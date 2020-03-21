import graphene
from graphene_django.types import DjangoObjectType
from contacts.models import Person

'''
NOTE:   It is not possible to use 'DjangoObjectType' with Neomodels since they do not inherit from Django base models.
        For this reason we have to use the basic 'ObjectType' for Neomodels here. 
'''

class PersonType(graphene.ObjectType):
    mobile_phone = graphene.String()
    uid = graphene.String()

class AddPerson(graphene.Mutation):
    person = graphene.Field(PersonType)

    class Arguments:
        mobile_phone = graphene.String(required=True)

    def mutate(self, info, mobile_phone):
        person = Person(
            mobile_phone=mobile_phone,
        )
        person.save()

        return AddPerson(person=person)

class Mutation(graphene.ObjectType):
    add_person = AddPerson.Field()

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
    query = Query,
    mutation = Mutation
)