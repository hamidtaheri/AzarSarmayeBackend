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

from api.schema.query import *


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


class CreateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        profile_id = graphene.Int(required=True, description='کاربر تراکنش')
        date = graphene.Date(required=True)
        amount = graphene.Int(required=True)
        transact_types = Transaction_Type_Enum(required=True)

    def mutate(self, info, user_id, date, amount, transact_type):
        # user = User.objects.get(id=user_id)
        profile = Profile.objects.get(id=user_id)
        tr = Transaction_old.objects.create(profule=profile, amount=amount, date=date, type=transact_type.value)

        return CreateTransaction(transaction=tr)


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


class UpdateProfilePayload(CreateProfilePayload):
    pass


class UpdateProfile(graphene.Mutation):
    """
    بنابه دلایلی از اینجا نام کاربری و کلمه عبور را نمیتوان تغییر داد
    """
    class Arguments:
        input_data = UpdateProfileInput(required=True, name="input")

    Output = UpdateProfilePayload

    @permission_required("can_add_profile")
    def mutate(self, info, input_data: UpdateProfileInput):
        current_user: User = info.context.user
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

            setattr(new_profile, k, v)

        # new_user.save()
        new_profile.save()
        return UpdateProfilePayload(profile=new_profile)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_transaction = CreateTransaction.Field()
    create_user = CreateUser.Field(description='ایجاد کاربر')
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
    # create_tarakonesh = CreateTarakonesh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
