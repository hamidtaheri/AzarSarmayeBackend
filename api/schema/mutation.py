from datetime import timezone

import graphql_jwt
from graphql_jwt.exceptions import PermissionDenied

from api.models import User, Transaction_old
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
        user_id = graphene.Int(required=True, description='کاربر تراکنش')
        date = graphene.Date(required=True)
        amount = graphene.Int(required=True)
        transact_types = Transaction_Type_Enum(required=True)

    def mutate(self, info, user_id, date, amount, transact_type):
        user = User.objects.get(id=user_id)
        tr = Transaction_old.objects.create(user=user, amount=amount, date=date, type=transact_type.value)

        return CreateTransaction(transaction=tr)


# class CreateTarakonesh(graphene.Mutation):
#     tarakonesh: Transaction = graphene.Field(type=Transaction,description='ایجاد تراکنش مالی')
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
