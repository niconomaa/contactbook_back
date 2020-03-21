import graphene

class Query(graphene.ObjectType):
    name = 'Query'
    description = '...'

    hello = graphene.String()

    def resolve_hello(root, info):
        return 'World'

schema = graphene.Schema(
    query = Query
)