import graphene
from contacts.schema import Query as contacts_query
from contacts.schema import Mutation as contacts_mutation

class QueryType(contacts_query):
    pass

class MutationType(contacts_mutation):
    pass

schema = graphene.Schema(
    query = QueryType,
    mutation=MutationType
)