import datetime

import django_jalali.db.models
import graphene
import graphql_jwt
import jdatetime
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from graphene import relay, Enum
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, staff_member_required
from graphql_jwt.shortcuts import get_token
from .models import *


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "body", "is_public", "owner")
        interfaces = (relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        filter_fields = ['id', 'last_name', 'mobile', ]
        interfaces = (relay.Node,)


class TransactionType(DjangoObjectType):
    shamse_date = graphene.String()

    # def resolve_j_date(root: Transaction, info):
    #     root.date.togregorian()
    #     return root.date.togregorian()

    def resolve_shamse_date(root: Transaction, info):
        return jdatetime.date.fromgregorian(date=root.date).strftime(format="%Y-%m-%d")

    class Meta:
        model = Transaction
        # exclude = ("created", "created_by", "modified", "modified_by")
        # exclude = ("created", "created_by", "modified", "modified_by")


class TransactionTypeEnum(Enum):
    variz = "Variz"
    bardasht = "Bardasht"


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    hello = graphene.String(default_value="Hi!")
    posts = graphene.List(PostType)
    # users = graphene.List(UserType)
    users = DjangoFilterConnectionField(UserType)
    transactions = graphene.List(TransactionType)

    @login_required
    def resolve_me(root, info, **kwargs):
        user = info.context.user
        return user

    def resolve_posts(root, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            return Post.objects.filter(Q(is_public=True) | Q(owner=user))

        return Post.objects.filter(is_public=True)

    @staff_member_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_transactions(root, info, **kwargs):
        user: get_user_model() = info.context.user
        # if user.is_anonymous or user is None:
        #     raise Exception(HAVE_NOT_PERMISSION)

        # if user.has_perm('can_view_transaction_for_all'):
        #     filter =
        transactions = Transaction.objects.all()
        return transactions


# ----------------

class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise PermissionDenied()
        else:
            token = get_token(user)
        return Login(user=user, token=token)


class CreateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        user_id = graphene.Int(required=True, description='کاربر تراکنش')
        date = graphene.Date(required=True)
        amount = graphene.Int(required=True)
        transact_type = TransactionTypeEnum(required=True)

    def mutate(self, info, user_id, date, amount, transact_type):
        user = User.objects.get(id=user_id)
        tr = Transaction.objects.create(user=user, amount=amount, date=date, type=transact_type.value)

        return CreateTransaction(transaction=tr)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_transaction = CreateTransaction.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()