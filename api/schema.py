import graphene
from graphene import relay
from django.db.models import Q
from graphene_django import DjangoObjectType

from .models import Post, User


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "body","is_public" ,"owner")
        interfaces = (relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    posts = graphene.List(PostType)
    users = graphene.List(UserType)

    def resolve_posts(root, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            return Post.objects.filter(Q(is_public=True) | Q(owner=user))

        return Post.objects.filter(is_public=True)

        def resolve_users(root, info, **kwargs):
            return User.objects.all()
