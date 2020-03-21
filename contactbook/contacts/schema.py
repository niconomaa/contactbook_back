import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User

"""
class Query(graphene.ObjectType):
    name = 'Query'
    description = '...'

    hello = graphene.String()

    def resolve_hello(root, info):
        return 'World'

schema = graphene.Schema(
    query = Query
) """

class UserType(DjangoObjectType):
    class Meta:
        model = User

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

class Query(graphene.ObjectType):
    name = 'Query'
    description = '...'

    user = graphene.List(
        UserType
    )

    def resolve_user(self, info, **kwargs):
        return User.objects.all()

schema = graphene.Schema(
    query = Query,
    mutation = Mutation
)