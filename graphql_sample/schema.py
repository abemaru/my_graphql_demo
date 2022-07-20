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
        filter_fields = ['name', 'description', 'brand', 'user__username']
        interfaces = (relay.Node,)


class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        brand = graphene.String()
        user = graphene.Int()

    item = graphene.Field(ItemType)

    def mutate(root, info, name, description, brand, user):
        user = User.objects.get(pk=user)
        item = Item(name=name, description=description, brand=brand, user=user)
        item.save()
        return CreateItem(item=item)


class DeleteItem(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, name):
        item = Item.objects.filter(name=name)
        item.delete()
        return DeleteItem(ok=True)


class UpdateItemUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        user = graphene.Int()

    ok = graphene.Boolean()

    def mutate(root, info, name, user):
        obj, _ = Item.objects.get_or_create(
            name=name,
            user_id=user
        )
        return UpdateItemUser(ok=True)


class MyMutation(graphene.ObjectType):
    create_item = CreateItem.Field()
    delete_item = DeleteItem.Field()
    update_item_user = UpdateItemUser.Field()


class Query(graphene.ObjectType):
    user = graphene.List(UserType, id=graphene.Int())
    item = graphene.List(ItemType, id=graphene.Int())

    all_user = DjangoFilterConnectionField(UserType)
    all_item = DjangoFilterConnectionField(ItemType)

    def resolve_user(self, info, **kwargs):
        return User.objects.all()

    def resolve_item(self, info, **kwargs):
        return Item.objects.all()


schema = graphene.Schema(query=Query, mutation=MyMutation)
