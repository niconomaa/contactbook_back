import graphene
from graphene_django.types import DjangoObjectType
from contacts.models import Contact

'''
NOTE:   It is not possible to use 'DjangoObjectType' with Neomodels since they do not inherit from Django base models.
        For this reason we have to use the basic 'ObjectType' for Neomodels here. 
'''

class ContactType(graphene.ObjectType):
    first_name = graphene.String()


class Query(graphene.ObjectType):
    all_contacts = graphene.List(ContactType)

    def resolve_all_contacts(self, info, **kwargs):
        return Contact.nodes.all()


schema = graphene.Schema(
    query = Query
)