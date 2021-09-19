import datetime
from django.db.models import Avg, Count, Min, Sum
import django_jalali.db.models
import graphene
import graphql_jwt
import jdatetime
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django_filters import OrderingFilter
from graphene import relay, Enum
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, staff_member_required
from graphql_jwt.shortcuts import get_token

from .models import *


class count_sum_tarakonesh_ConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    total_sum = graphene.Float()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

    def resolve_total_sum(self, info, **kwargs):
        r = self.iterable.aggregate(Mablagh_sum=Sum('Mablagh'))
        return r['Mablagh_sum']


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "body", "is_public", "owner")
        interfaces = (relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        # exclude = ("password",)
        # filter_fields = ['id', 'last_name', 'mobile', ]
        # interfaces = (relay.Node,)
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'shakhs', 'last_login')


class TransactionType(DjangoObjectType):
    shamse_date = graphene.String()

    # def resolve_j_date(root: Transaction, info):
    #     root.date.togregorian()
    #     return root.date.togregorian()

    def resolve_shamse_date(self: Transaction, info):
        return jdatetime.date.fromgregorian(date=self.date).strftime(format="%Y-%m-%d")

    class Meta:
        model = Transaction
        # exclude = ("created", "created_by", "modified", "modified_by")
        # exclude = ("created", "created_by", "modified", "modified_by")


class Transaction_Type_Enum(Enum):
    variz = "Variz"
    bardasht = "Bardasht"


class MoarefiShodeHaType(DjangoObjectType):
    class Meta:
        model = Ashkhas
        exclude = ('seporde', 'tarakoneshha', 'Moaref_Tbl_Ashkhas_id',)


class AshkhasType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    seporde = graphene.Float(source='seporde')  # اتصال به @property
    moarefi_shode_ha = graphene.List(of_type=MoarefiShodeHaType)
    moaref = graphene.String(description='معرف')

    def resolve_moarefi_shode_ha(self: Ashkhas, info):
        current_user: User = info.context.user
        return Ashkhas.objects.filter(Moaref_Tbl_Ashkhas_id=self).all()

    def resolve_moaref(self: Ashkhas, info):
        return f'{self.Moaref_Tbl_Ashkhas_id.Fname} {self.Moaref_Tbl_Ashkhas_id.Lname}'

    class Meta:
        model = Ashkhas
        exclude = ('MorefiBekhod2', 'Moaref_Tbl_Ashkhas_id',)
        filter_fields = {
            'id': ['exact'],
            'Lname': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        # if info.context.user.is_anonymous:
        #     return queryset.filter(published=True)
        return queryset


class TarakoneshType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Tarakonesh
        fields = ('shakhs', 'Tarikh_Moaser', 'date_time', 'Mablagh', 'DarMelyoon', 'kind', 'Des',)
        filter_fields = {'shakhs__id': ['exact'],
                         'date_time': ['lte', 'gte', 'range'],
                         'kind__id': ['exact'], }
        # exclude = ('tarikh')
        connection_class = count_sum_tarakonesh_ConnectionBase
        interfaces = (relay.Node,)

        # order_by = OrderingFilter(
        #     fields=('date_time')
        # )


class TransactionKindType(DjangoObjectType):
    class Meta:
        model = TransactionKind
        fields = ['id', 'title']
        # exclude = ('id',)
        filter_fields = {'id': ['exact']}


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    # hello = graphene.String(default_value="Hi!")
    posts = graphene.List(PostType)
    # users = graphene.List(UserType)
    # users = DjangoFilterConnectionField(UserType)
    users = graphene.List(UserType)
    last_logged_in_users = graphene.List(UserType)
    transactions = graphene.List(TransactionType)
    ashkhas = DjangoFilterConnectionField(AshkhasType)
    tarakoneshs = DjangoFilterConnectionField(TarakoneshType)
    transaction_kinds = graphene.List(TransactionKindType)

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

    @staff_member_required
    def resolve_last_logged_in_users(root, info, **kwargs):
        return User.objects.order_by('-last_login')[0:10]

    @login_required
    def resolve_transactions(root, info, **kwargs):
        user: get_user_model() = info.context.user
        # if user.is_anonymous or user is None:
        #     raise Exception(HAVE_NOT_PERMISSION)

        # if user.has_perm('can_view_transaction_for_all'):
        #     filter =
        transactions = Transaction.objects.all()
        return transactions

    @login_required
    def resolve_ashkhas(self, info, **kwargs):
        current_user: User = info.context.user
        if current_user.is_superuser:
            return Ashkhas.objects.all()
        else:
            t = Ashkhas.objects.filter(user=current_user)
            return t

    def resolve_tarakoneshs(self, info, **kwargs):
        current_user: User = info.context.user
        if current_user.is_superuser:
            return Tarakonesh.objects.all()
        else:
            tr = Tarakonesh.objects.filter(shakhs__user=current_user)
            return tr

    def resolve_transaction_kinds(root, info):
        return TransactionKind.objects.all()


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
        transact_types = Transaction_Type_Enum(required=True)

    def mutate(self, info, user_id, date, amount, transact_type):
        user = User.objects.get(id=user_id)
        tr = Transaction.objects.create(user=user, amount=amount, date=date, type=transact_type.value)

        return CreateTransaction(transaction=tr)


# class CreateTarakonesh(graphene.Mutation):
#     tarakonesh: Tarakonesh = graphene.Field(type=Tarakonesh,description='ایجاد تراکنش مالی')
#
#     class Arguments:
#         user


class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_transaction = CreateTransaction.Field()
    # create_tarakonesh = CreateTarakonesh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
