import graphene
from django.db.models import Q
from graphene import relay, Enum, Int, Date
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, staff_member_required

from api.models import *


class count_sum_tarakonesh_ConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    total_sum = graphene.Float()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

    def resolve_total_sum(self, info, **kwargs):
        r = self.iterable.aggregate(Mablagh_sum=Sum('amount'))
        return r['Mablagh_sum']


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "body", "is_public", "owner")
        interfaces = (relay.Node,)


class UserType(DjangoObjectType):
    """
    me
    """

    class Meta:
        model = User
        # exclude = ("password",)
        # filter_fields = ['id', 'last_name', 'mobile', ]
        # interfaces = (relay.Node,)
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'profile', 'last_login')


class Transaction_Type_Enum(Enum):
    variz = "Variz"
    bardasht = "Bardasht"


class MoarefiShodeHaType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


class ProfitCalculateType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    description = graphene.String()

    class Meta:
        model = ProfitCalculate
        fields = ('amount', 'date_from', 'date_to', 'percent', 'calculated_amount', 'days',)

    def resolve_description(self, info):
        return self


class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = ['id', 'description', 'kind', 'image', ]


class ProfileType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    seporde = graphene.Float(source='seporde')  # اتصال به @property
    moarefi_shode_ha = graphene.List(of_type=MoarefiShodeHaType)
    moaref = graphene.String(description='معرف')
    images = graphene.List(of_type=ImageType)
    mohasebe_sod = graphene.List(ProfitCalculateType,
                                 description='نمایش جزیات محاسبه سود از تاریخ تا تاریخ برای کاربر جاری',
                                 az_date=Date(required=True, description='از تاریخ'),
                                 ta_date=Date(required=True, description='تا تاریخ'),
                                 )
    sum_of_sod = graphene.Float(
        description='مجموع سود از تاریخ تا تاریخ برای کاربر جاری',
        az_date=Date(required=True, description='از تاریخ'),
        ta_date=Date(required=True, description='تا تاریخ'),
    )

    class Meta:
        model = Profile
        fields = (
            'id', 'user', 'first_name', 'last_name', 'code_meli', 'adress', 'shomare_kart', 'shomare_hesab',
            'description', 'tel', 'mobile1', 'transactions', 'images')
        filter_fields = {
            'id': ['exact'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'code_meli': ['exact', 'icontains', 'istartswith'],
            'mobile1': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)

    # @staff_member_required
    def resolve_moarefi_shode_ha(self: Profile, info):
        current_user: User = info.context.user
        return Profile.objects.filter(presenter=self).all()

    def resolve_moaref(self: Profile, info):
        moaref = self.presenter or ''
        return moaref

    def resolve_images(self, info):
        current_user: User = info.context.user
        prof: Profile = self
        # imgs = Profile.images
        ct = ContentType.objects.get_for_model(self)

        images = Image.objects.filter(content_type=ct, object_id=self.id)
        return images

    def resolve_mohasebe_sod(self: Profile, info, az_date, ta_date):
        current_user: User = info.context.user
        user: Profile = Profile()
        if current_user.is_superuser:
            user = self
        else:
            user = Profile.objects.get(user=current_user)

        r, _ = user.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
        return r

    def resolve_sum_of_sod(self, info, az_date, ta_date):
        current_user: User = info.context.user
        user: Profile = Profile()
        if current_user.is_superuser:
            user = self
        else:
            user = Profile.objects.get(user=current_user)

        r, sum_sod = user.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
        return sum_sod

    @classmethod
    def get_queryset(cls, queryset, info):
        # if info.context.user.is_anonymous:
        #     return queryset.filter(published=True)
        return queryset


class TransactionType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Transaction
        fields = ('profile', 'Tarikh_Moaser', 'date_time', 'amount', 'percent', 'kind', 'description',)
        filter_fields = {'profile__id': ['exact'],
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
    last_logged_in_users = graphene.List(UserType, count=Int())
    profiles = DjangoFilterConnectionField(ProfileType)
    transactions = DjangoFilterConnectionField(TransactionType)
    transaction_kinds = graphene.List(TransactionKindType)
    mohasebe_sod = graphene.List(ProfitCalculateType,
                                 description='نمایش سود از تاریخ تا تاریخ برای کاربر',
                                 user_id=Int(required=True, description='کابر'),
                                 az_date=Date(required=True, description='از تاریخ'),
                                 ta_date=Date(required=True, description='تا تاریخ'),
                                 )

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
    def resolve_last_logged_in_users(root, count, info, **kwargs):
        return User.objects.order_by('-last_login')[0:10]

    @login_required
    def resolve_transactions(root, info, **kwargs):
        user: get_user_model() = info.context.user
        # if user.is_anonymous or user is None:
        #     raise Exception(HAVE_NOT_PERMISSION)

        # if user.has_perm('can_view_transaction_for_all'):
        #     filter =
        transactions = Transaction_old.objects.all()
        return transactions

    @login_required
    def resolve_profiles(self, info, **kwargs):
        current_user: User = info.context.user
        if current_user.is_superuser:
            return Profile.objects.all()
        else:
            t = Profile.objects.filter(user=current_user)
            return t

    def resolve_tarakoneshs(self, info, **kwargs):
        current_user: User = info.context.user
        if current_user.is_superuser:
            return Transaction.objects.all()
        else:
            tr = Transaction.objects.filter(shakhs__user=current_user)
            return tr

    def resolve_transaction_kinds(root, info):
        return TransactionKind.objects.all()

    @login_required
    def resolve_mohasebe_sod(root, info, user_id, az_date, ta_date):
        current_user: User = info.context.user
        user: Profile = Profile()
        if current_user.is_superuser:
            user = Profile.objects.get(id=user_id)
        else:
            user = Profile.objects.get(user=current_user)

        r, _ = user.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
        return r