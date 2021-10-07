import graphql_jwt
from django.contrib.auth import authenticate
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


class profileInput(graphene.InputObjectType):
    id = graphene.ID()
    user_id = Int(required=False, description='کاربر متناظر')
    first_name = String()
    last_name = String()
    code_meli = String()
    file = Upload(required=True)


class CreateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        input = profileInput(required=True)

    @permission_required("can_add_profile")
    def mutate(self, info, input: profileInput):
        current_user: User = info.context.user
        new_profile: Profile = Profile()
        if input.user_id is not None:
            try:
                user = User.objects.get(id=input.user_id)
            except:
                user = None
            new_profile.user = user
        new_profile.first_name = input.first_name
        new_profile.last_name = input.last_name
        new_profile.code_meli = input.code_meli
        # for k, v in input.items():
        #     setattr(new_profile, k, v)

        new_profile.save()
        return CreateProfile(new_profile)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_transaction = CreateTransaction.Field()
    create_user = CreateUser.Field(description='ایجاد کاربر')
    create_profile = CreateProfile.Field()
    # create_tarakonesh = CreateTarakonesh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token = graphql_jwt.Revoke.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
