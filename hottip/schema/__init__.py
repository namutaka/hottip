import graphene
from . import queries, mutations

class Query(queries.Query, graphene.ObjectType):
    pass

class Mutation(mutations.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

