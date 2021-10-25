import graphene
import graphql_jwt
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.utils import timezone
from graphene import String, ID
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import permission_required
from graphql_jwt.exceptions import PermissionDenied
from graphql_jwt.shortcuts import get_token
from graphene_file_upload.scalars import Upload

from api.schema.query import *
# from settings import HAVE_NOT_PERMISSION
HAVE_NOT_PERMISSION = 'you have not permission !!'
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
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            token = get_token(user)
        return Login(user=user, token=token)


class CreateImageInput(graphene.InputObjectType):
    image = Upload(required=True)
    kind_id = graphene.Int()
    description = graphene.String()


class createImagePayload(graphene.ObjectType):
    image = graphene.Field(ImageType, required=True)


class UpdateImageInput(CreateImageInput):
    image = Upload(required=False)
    id = graphene.ID(required=True)


class UpdateImagePayload(CreateImageInput):
    pass


# class UpdateImage(graphene.Mutation):
#     class Arguments:
#         input_data = UpdateImageInput(required=True, name="input")


class CreateTransactionInput(graphene.InputObjectType):
    """
        ورودی های لازم برای ایجاد تراکنش
    """
    profile_id = graphene.Int(required=True, description='کاربر تراکنش')
    effective_date = graphene.Date(required=True, description='تاریخ موثر')
    amount = graphene.Int(required=True, description='مبلغ')
    kind_id = graphene.Int(required=True, description='id نوع تراکنش')
    description = String(description='توضیحات')


class CreateTransactionPayload(graphene.ObjectType):
    transaction = graphene.Field(TransactionType, required=True)


class CreateTransaction(graphene.Mutation):
    """
    ایجاد تراکنش
    """

    class Arguments:
        input_data = CreateTransactionInput(required=True, name="input")

    Output = CreateTransactionPayload

    @login_required
    def mutate(self, info, input_data: CreateTransactionInput):
        current_user: User = info.context.user
        profile = Profile.objects.get(id=input_data.profile_id)
        if not current_user.has_perm('add_transaction_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            profile = Profile.objects.get(user=current_user)
        tr = Transaction.objects.create(profile=profile, amount=input_data.amount,
                                        effective_date=input_data.effective_date,
                                        kind_id=input_data.kind_id, description=input_data.description,
                                        created_by=current_user, date_time=now(), percent=0)

        return CreateTransactionPayload(transaction=tr)


class UpdateTransactionInput(graphene.InputObjectType):
    """
    مبلغ را نمیتوان به روز کرد
    """
    id = graphene.ID(required=True)

    profile_id = graphene.Int(required=True, description='کاربر تراکنش')
    effective_date = graphene.Date(required=True, description='تاریخ موثر')
    # amount = graphene.Int(required=True, description='مبلغ')
    kind_id = graphene.Int(required=True, description='id نوع تراکنش')
    description = String(description='توضیحات')


class UpdateTransactionPayload(CreateTransactionPayload):
    pass


class UpdateTransaction(graphene.Mutation):
    class Arguments:
        input_data = UpdateTransactionInput(required=True, name="input")

    Output = UpdateTransactionPayload

    def mutate(self, info, input_data: UpdateTransactionInput):
        current_user: User = info.context.user
        profile = Profile.objects.get(id=input_data.profile_id)
        if not current_user.has_perm('add_transaction_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            if profile.user != current_user:
                raise MyException(HAVE_NOT_PERMISSION)
            profile = Profile.objects.get(user=current_user)
        transaction = Transaction.objects.get(id=input_data.id, profile=profile)
        transaction.profile = profile
        transaction.effective_date = input_data.effective_date
        transaction.kind_id = input_data.kind_id
        transaction.description = input_data.description
        transaction.modified_by = current_user
        transaction.modified = now()
        transaction.save()

        return UpdateTransactionPayload(transaction=transaction)


class UserInput(graphene.InputObjectType):
    id = ID()
    username = String(required=True)
    password = String(required=True)
    email = String()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserInput(required=True)

    @permission_required("can-add_user")
    def mutate(self, info, input):
        current_user: User = info.context.user
        # if not current_user.has_perm(""):
        #     raise Exception(HAVE_NOT_PERMISSION)
        new_user: User = User(username=input.username, email=input.email)
        new_user.set_password(input.password)
        new_user.save()

        return CreateUser(user=new_user)


class CreateProfileInput(graphene.InputObjectType):
    # id = graphene.ID()
    # user_id = Int(required=False, description='کاربر متناظر')
    user = UserInput(required=True).Field()
    first_name = String()
    last_name = String()
    code_meli = String()
    adress = String()
    shomare_kart = String()
    shomare_hesab = String()
    presenter_id = Int(required=False, description='id معرف')
    description = String()
    tel = String()
    mobile1 = String()
    mobile2 = String()
    images = graphene.List(CreateImageInput)
    # file = Upload(required=True)


class CreateProfilePayload(graphene.ObjectType):
    profile = graphene.Field(ProfileType, required=True)


class CreateProfile(graphene.Mutation):
    """
    نام کاربری و کلمه عبور معرفی شده برای ساخت کاربر جدید و اتصال آن به پروفایل درحال ساخت استفاده میشود
    """

    class Arguments:
        input_data = CreateProfileInput(required=True, name="input")

    Output = CreateProfilePayload

    @permission_required("can_add_profile")
    def mutate(self, info, input_data: CreateProfileInput):
        current_user: User = info.context.user
        new_profile: Profile = Profile()

        # حلقه برای ست کردن مقادیر به جز مقادیر خاص که لازم است کنترل شوند
        for k, v in input_data.items():
            if k == 'user':
                try:
                    new_user: User = User(username=input_data.user.username)
                    new_user.set_password(raw_password=input_data.user.password)
                    # new_user.save()
                    # new_profile.user = new_user
                except IntegrityError as e:
                    raise MyException('نام کاربری تکراری است')
                continue
            if k == 'presenter_id':
                try:
                    presenter: Profile = Profile.objects.get(id=input_data.presenter_id)
                    # new_profile.presenter = presenter
                except Profile.DoesNotExist:
                    raise MyException('معرف پیدا نشد')

            setattr(new_profile, k, v)

        new_user.save()
        new_profile.user = new_user

        new_profile.save()
        return CreateProfilePayload(profile=new_profile)


class UpdateProfileInput(CreateProfileInput):
    id = graphene.ID(required=True)
    user = UserInput(required=False).Field()  # در به روزرسانی کابر اجباری نیست
    images = graphene.List(UpdateImageInput)


class UpdateProfilePayload(CreateProfilePayload):
    pass


class UpdateProfile(graphene.Mutation):
    """
    بنابه دلایلی از اینجا نام کاربری و کلمه عبور را نمیتوان تغییر داد
    """

    class Arguments:
        input_data = UpdateProfileInput(required=True, name="input")

    Output = UpdateProfilePayload

    @login_required
    def mutate(self, info, input_data: UpdateProfileInput):
        current_user: User = info.context.user
        if not current_user.has_perm('can_edit_profile_for_all'):  # کاربر دسترسی ندارد
            #  فیلتر بر اساس کاربر جاری
            new_profile = Profile.objects.get(user=current_user)
        else:
            try:
                new_profile: Profile = Profile.objects.get(id=input_data.id)
            except Profile.DoesNotExist:
                raise MyException('پروفایل وچود ندارد')

        # حلقه برای ست کردن مقادیر به جز مقادیر خاص که لازم است کنترل شوند
        for k, v in input_data.items():
            if k == 'user':
                try:
                    new_user: User = User.objects.get(username=new_profile.user)
                    # new_user.username = input_data.user.username
                    # new_user.set_password(raw_password=input_data.user.password)
                    # new_user.save()
                    # new_profile.user = new_user
                except IntegrityError as e:
                    raise MyException('نام کاربری تکراری است')
                except User.DoesNotExist:
                    raise MyException('کاربر وجود ندارد')
                continue
            if k == 'presenter_id':
                try:
                    presenter: Profile = Profile.objects.get(id=input_data.presenter_id)
                    # new_profile.presenter=presenter
                except Profile.DoesNotExist:
                    raise MyException('معرف پیدا نشد')
            if k == 'images':
                for img in input_data.images:
                    new_img = Image.objects.get_or_create(id=img.id, object_id=new_profile.id, content_type_id=4)[0]
                    for ki, vi in img.items():
                        setattr(new_img, ki, vi)
                    new_img.save()

                continue
            setattr(new_profile, k, v)

        # new_user.save()
        new_profile.save()
        return UpdateProfilePayload(profile=new_profile)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()
    create_user = CreateUser.Field(description='ایجاد کاربر')
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
    # create_tarakonesh = CreateTarakonesh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
