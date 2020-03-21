import graphene
from graphene_django.types import DjangoObjectType
from contacts.models import Person

'''
NOTE:   It is not possible to use 'DjangoObjectType' with Neomodels since they do not inherit from Django base models.
        For this reason we have to use the basic 'ObjectType' for Neomodels here. 
'''

class PersonType(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    mobile_phone = graphene.String()
    email = graphene.String()


class Query(graphene.ObjectType):
    all_persons = graphene.List(PersonType)

    def resolve_all_persons(self, info, **kwargs):
        # Use 'Person.nodes' instead of 'Person.objects' here
        return Person.nodes.all()


schema = graphene.Schema(
    query = Query
)