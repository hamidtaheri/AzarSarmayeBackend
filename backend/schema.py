import graphene

from api.schema import mutation, query


class Query(query.Query, graphene.ObjectType):
    pass


class Mutation(mutation.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
