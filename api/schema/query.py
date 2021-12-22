import graphene
from django.contrib.auth.models import Group, Permission
from django_fsm import get_available_FIELD_transitions
from django_fsm_log.models import StateLog
from graphene import relay, Enum, Int, Date, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, staff_member_required

from api import views
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
    اطلاعات کاربر جاری
    """

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'profile', 'last_login', 'user_permissions',)
        # groups


class Transaction_Type_Enum(Enum):
    variz = "Variz"
    bardasht = "Bardasht"


class MoarefiShodeHaType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


class WorkFlowHistoryType(DjangoObjectType):
    class Meta:
        model = StateLog


class ProfitCalculateType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    description = graphene.String()

    class Meta:
        model = ProfitCalculate
        fields = ('amount', 'date_from', 'date_to', 'percent', 'calculated_amount', 'days', 'profile')

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
    presenter = graphene.String(description='معرف')
    presenter_id = graphene.Int(description='معرف id')
    state = graphene.String(description='مرحله در گردش کار')
    state_history = graphene.List(of_type=WorkFlowHistoryType)
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
    workflow_transition = graphene.List(of_type=graphene.String, description='مرحله بعدی در گردش کار')
    province_id = graphene.Int(required=False)

    class Meta:
        model = Profile
        fields = (
            'id', 'user', 'first_name', 'last_name', 'father_name', 'birth_place', 'national_code',
            'id_number', 'birth_date',
            'account_number', 'sheba', 'card_number', 'bank',
            'address', 'city', 'postal_code', 'tel', 'home_phone', 'office_phone', 'mobile1', 'mobile2', 'email',
            'description', 'transactions', 'images',
        )
        filter_fields = {
            'id': ['exact'],
            'presenter__id': ['exact'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'national_code': ['exact', 'icontains', 'istartswith'],
            'mobile1': ['exact', 'icontains', 'istartswith'],
            'state': ['in']
        }
        interfaces = (relay.Node,)

    # @staff_member_required
    def resolve_moarefi_shode_ha(self: Profile, info):
        current_user: User = info.context.user
        return Profile.objects.filter(presenter=self).all()

    def resolve_presenter(self: Profile, info):
        moaref = self.presenter or ''
        return moaref

    def resolve_presenter_id(self: Profile, info):
        moaref = self.presenter.id or ''
        return moaref

    def resolve_images(self, info):
        current_user: User = info.context.user
        prof: Profile = self
        # imgs = Profile.images
        ct = ContentType.objects.get_for_model(self)

        images = Image.objects.filter(content_type=ct, object_id=self.id)
        return images

    def resolve_state(self, info):
        return self.state

    def resolve_state_history(self, info):
        return StateLog.objects.for_(self)

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

    def resolve_workflow_transition(self, info):
        current_user: User = info.context.user
        avail_user_trans = self.get_available_user_state_transitions(user=current_user)
        avail_user_trans_list = list(avail_user_trans)
        attr = (o.name for o in avail_user_trans_list)
        return attr

    def resolve_province_id(self, info):
        p: Profile = self
        return p.city.province.id

    @classmethod
    def get_queryset(cls, queryset, info):
        # if info.context.user.is_anonymous:
        #     return queryset.filter(published=True)
        return queryset


class MohasebeSodForAllSummaryType(ObjectType):
    profile = graphene.Field(ProfileType)
    amount = graphene.Float()

    def resolve_amount(self, info):
        return self[1]

    def resolve_profile(self, info):
        return self[0]


class TransactionRequestType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = TransactionRequest
        fields = ('transaction', 'kind', 'created', 'description')
        filter_fields = {'id': ['exact'], 'transaction__id': ['exact'], 'kind__id': ['exact'], }
        interfaces = (relay.Node,)


class TransactionRequestKindType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = TransactionRequestKind
        fields = ['id', 'title', 'description', ]


class TransactionType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    amount = graphene.Float(required=True, description='مبلغ')
    images = graphene.List(of_type=ImageType)

    class Meta:
        model = Transaction
        fields = (
            'profile', 'effective_date', 'date_time', 'amount', 'percent', 'kind', 'description', 'images',
            'contract_term', 'expire_date', 'alias')
        filter_fields = {'id': ['exact'], 'profile__id': ['exact'],
                         'effective_date': ['lte', 'gte', 'range'],
                         'kind__id': ['exact'], }
        # exclude = ('tarikh')
        connection_class = count_sum_tarakonesh_ConnectionBase
        interfaces = (relay.Node,)

        # order_by = OrderingFilter(
        #     fields=('date_time')
        # )

    def resolve_amount(self, info):
        return self.amount

    def resolve_images(self, info):
        current_user: User = info.context.user
        transaction: Transaction = self
        ct = ContentType.objects.get_for_model(self)

        images = Image.objects.filter(content_type=ct, object_id=self.id)
        return images


class TransactionKindType(DjangoObjectType):
    class Meta:
        model = TransactionKind
        fields = ['id', 'title']
        # exclude = ('id',)
        filter_fields = {'id': ['exact']}


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = ['name', 'content_type', 'codename']
        filter_fields = {'id': ['exact'], 'name': ['icontains']}


class GroupType(DjangoObjectType):
    users = graphene.List(UserType)

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'users']
        filter_fields = {'id': ['exact'], 'name': ['icontains', 'istartswith']}

    def resolve_users(self: Group, info):
        users = self.user_set.all()
        return users


class CityType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = City
        fields = ('name', 'id')
        filter_fields = {'province__id': ['exact'], 'name': ['icontains', 'istartswith']}
        interfaces = (relay.Node,)


class ProvinceType(DjangoObjectType):
    class Meta:
        model = Province
        fields = ['name', 'id', 'cites', ]


# class WorkflowSatesType:
#     class Meta:
#         model = WorkFlowStates
#
def allowed_workflow_sates(user: User) -> list:
    workflow_sates = []
    if user.has_perm('api.START_WF_STATE'):
        workflow_sates.append('start')
    if user.has_perm('api.CONVERTED_WF_STATE'):
        workflow_sates.append('converted')
    if user.has_perm('api.STUFF_ADDED_WF_STATE'):
        workflow_sates.append('staff_added')
    if user.has_perm('api.CUSTOMER_ADDED_WF_STATE'):
        workflow_sates.append('customer_added')
    if user.has_perm('api.STUFF_CHECKED_WF_STATE'):
        workflow_sates.append('stuff_checked')
    if user.has_perm('api.STUFF_CONFIRMED_WF_STATE'):
        workflow_sates.append('stuff_confirmed')
    if user.has_perm('api.CUSTOMER_CONFIRMED_WF_STATE'):
        workflow_sates.append('customer_confirmed')
    if user.has_perm('api.BOSS_CONFIRMED_WF_STATE'):
        workflow_sates.append('boss_confirmed')

    return workflow_sates


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    # hello = graphene.String(default_value="Hi!")
    posts = graphene.List(PostType)
    # users = graphene.List(UserType)
    # users = DjangoFilterConnectionField(UserType)
    # workflow_states = graphene.List(WorkflowSatesType)
    users = graphene.List(UserType)
    last_logged_in_users = graphene.List(UserType, count=Int())
    profiles = DjangoFilterConnectionField(ProfileType)

    transaction_request_kinds = graphene.List(TransactionRequestKindType)

    transaction_requests = DjangoFilterConnectionField(TransactionRequestType)
    transactions = DjangoFilterConnectionField(TransactionType)
    transaction_kinds = graphene.List(TransactionKindType)
    mohasebe_sod = graphene.List(ProfitCalculateType,
                                 description='نمایش سود از تاریخ تا تاریخ برای کاربر',
                                 profile_id=Int(required=True, description='کابر'),
                                 az_date=Date(required=True, description='از تاریخ'),
                                 ta_date=Date(required=True, description='تا تاریخ'),
                                 )
    mohasebe_sod_for_all_summary = graphene.List(MohasebeSodForAllSummaryType,
                                                 description='نمایش سود از تاریخ تا تاریخ برای  همه کاربران',
                                                 az_date=Date(required=True, description='از تاریخ'),
                                                 ta_date=Date(required=True, description='تا تاریخ'),
                                                 offset=Int(), first=Int()
                                                 )
    mohasebe_sod_all_export_excel = graphene.String(
        description='خروجی اکسل سود از تاریخ تا تاریخ برای  همه کاربران',
        az_date=Date(required=True, description='از تاریخ'),
        ta_date=Date(required=True, description='تا تاریخ'),
        offset=Int(), first=Int()
    )
    permissions = graphene.List(PermissionType, description='')
    groups = graphene.List(GroupType, description='گروه های دسترسی')
    provinces = graphene.List(ProvinceType)
    cities = DjangoFilterConnectionField(CityType)

    #################

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
    def resolve_transaction_requests(root, info):
        current_user: get_user_model() = info.context.user
        tr_reqs = TransactionRequest.objects.all()

        if not current_user.has_perm('api.view_all_TransactionRequests'):
            tr_reqs = tr_reqs.filter(transaction__profile__user=current_user)

        return tr_reqs

    @staticmethod
    def resolve_transaction_request_kinds(root, info, **kwargs):
        return TransactionRequestKind.objects.all()

    @login_required
    def resolve_transactions(root, info, **kwargs):
        current_user: get_user_model() = info.context.user
        # if user.is_anonymous or user is None:
        #     raise Exception(HAVE_NOT_PERMISSION)
        transactions = Transaction.objects.all()

        if not current_user.has_perm('api.view_all_transactions'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            transactions = transactions.filter(profile__user=current_user)

        return transactions

    @login_required
    def resolve_profiles(self, info, **kwargs):
        current_user: User = info.context.user
        profiles = Profile.objects.all()
        # p = Profile.objects.get(id=10)
        #
        # avail_trans = list(p.get_available_state_transitions())
        # all_trans = list(p.get_all_state_transitions())
        # avail_user_trans = p.get_available_user_state_transitions(user=current_user)
        # avail_user_trans_list = list(avail_user_trans)
        # print(avail_user_trans_list)
        # for t in avail_user_trans_list:
        #     print(t.name)

        if not current_user.has_perm('api.view_all_profiles'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            profiles = Profile.objects.filter(user=current_user)
        #     فیلتر پروفایل ها بر اساس دسترسی کاربر به مرحله در گردش کار
        allowed_workflow = allowed_workflow_sates(current_user)
        profiles = profiles.filter(state__in=allowed_workflow)  # "START",
        return profiles

    def resolve_transaction_kinds(root, info):
        return TransactionKind.objects.all()

    @login_required
    def resolve_mohasebe_sod(root, info, profile_id, az_date, ta_date):
        current_user: User = info.context.user
        p: Profile = Profile()
        if current_user.is_superuser:
            p = Profile.objects.get(id=profile_id)
        else:
            p = Profile.objects.get(user=current_user)

        r, _ = p.mohasebe_sod_old(az_date=az_date, ta_date=ta_date)
        return r

    @login_required
    def resolve_mohasebe_sod_for_all_summary(root, info, az_date, ta_date, offset, first):
        current_user: User = info.context.user
        sod_list: list[Profile, int] = []
        if current_user.is_superuser:
            for pr in Profile.objects.all()[offset: first]:
                p: Profile = pr
                _, sod_sum = mohasebe_sod_1_nafar(p.id, az_date, ta_date)
                sod_list.append((p, sod_sum))

            return sod_list

    @login_required
    def resolve_mohasebe_sod_all_export_excel(root, info, az_date, ta_date):
        return views.mohasebe_sod_all_export_excel(az_date=az_date, ta_date=ta_date)

    @staff_member_required
    def resolve_permissions(self, info, **kwargs):
        permissions = Permission.objects.all()
        return permissions

    @staff_member_required
    def resolve_groups(self, info, **kwargs):
        groups = Group.objects.all()
        return groups

    def resolve_provinces(root, info):
        return Province.objects.all()

    def resolve_cities(root, info, **kwargs):
        return City.objects.all()
