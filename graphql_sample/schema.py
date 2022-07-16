import graphene
from graphene_django import DjangoObjectType

from graphql_sample.models import User, Item

class UserType(DjangoObjectType):
    class Meta:
        model = User


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class Query(graphene.ObjectType):
    user = graphene.List(UserType, id=graphene.Int())
    item = graphene.List(ItemType, id=graphene.Int())

    def resolve_user(self, info, **kwargs):
        return User.objects.all()

    def resolve_item(self, info, **kwargs):
        return Item.objects.all()


schema = graphene.Schema(query=Query)
