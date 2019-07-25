import graphene
import messenger_analysis.messenger_analysis.schema

class Query(messenger_analysis.messenger_analysis.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(messenger_analysis.messenger_analysis.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)