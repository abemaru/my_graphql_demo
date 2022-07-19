import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_sample.models import User, Item

class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username']
        interfaces = (relay.Node,)


class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        filter_fields = ['name', 'description', 'brand']
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = graphene.List(UserType, id=graphene.Int())
    item = graphene.List(ItemType, id=graphene.Int())

    all_user = DjangoFilterConnectionField(UserType)
    all_item = DjangoFilterConnectionField(ItemType)

    def resolve_user(self, info, **kwargs):
        return User.objects.all()

    def resolve_item(self, info, **kwargs):
        return Item.objects.all()


schema = graphene.Schema(query=Query)
