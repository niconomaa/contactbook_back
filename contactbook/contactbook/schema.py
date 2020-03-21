import graphene
"""
# here: from application.schema import Query as application_query

class Query(here it will inherit from application_query):
    pass

schema = graphene.Schema(query=Query)
"""
class QueryType(graphene.ObjectType):
    name = 'Query'
    description = '...'

    hello = graphene.String()

    def resolve_hello(root, info):
        return 'World'

schema = graphene.Schema(
    query = QueryType
)