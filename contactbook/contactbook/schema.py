import graphene
from contacts.schema import Query as contacts_query

class QueryType(contacts_query):
    pass

schema = graphene.Schema(
    query = QueryType
)