import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from messenger_analysis.messenger_analysis.models import User, BlockedWord

# Create a GraphQL type for the user model
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Create a GraphQL type for the blockedword model
class BlockedWordType(DjangoObjectType):
    class Meta:
        model = BlockedWord

# Create a Query type
class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    blockedword = graphene.Field(BlockedWordType, word=graphene.String())
    users = graphene.List(UserType)
    blockedwords = graphene.List(BlockedWordType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_blockedword(self, info, **kwargs):
        word = kwargs.get('word')

        if word is not None:
            return BlockedWord.objects.get(word=word)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_blockedwords(self, info, **kwargs):
        return BlockedWord.objects.all()

# Create Input Object Types
class UserInput(graphene.InputObjectType):
    id = graphene.Int()

class BlockedWordInput(graphene.InputObjectType):
    users = graphene.List(UserInput)
    word = graphene.String()


# Create mutations for users
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(id=input.id)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(id=id)
        if user_instance:
            ok = True
            user_instance.id = input.id
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)

# Create mutations for Blocked Words
class CreateBlockedWord(graphene.Mutation):
    class Arguments:
        input = BlockedWordInput(required=True)

    ok = graphene.Boolean()
    blockedword = graphene.Field(BlockedWordType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        users = []
        for user_input in input.users:
          user = User.objects.get(id=user_input.id)
          if user is None:
            return CreateBlockedWord(ok=False, blockedword=None)
          users.append(user)
        blockedword_instance = BlockedWord(
            word=input.word
          )
        blockedword_instance.save()
        blockedword_instance.users.set(users)
        return CreateBlockedWord(ok=ok, blockedword=blockedword_instance)


class UpdateBlockedWord(graphene.Mutation):
    class Arguments:
        input = BlockedWordInput(required=True)

    ok = graphene.Boolean()
    blockedword = graphene.Field(BlockedWordType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        blockedword_instance = BlockedWord.objects.get(word=input.word)
        if blockedword_instance:
            ok = True
            users = []
            for user_input in input.users:
              user = User.objects.get(id=user_input.id)
              if user is None:
                return UpdateBlockedWord(ok=False, blockedword=None)
              users.append(user)
            blockedword_instance.word=input.word
            blockedword_instance.users.set(users)
            return UpdateBlockedWord(ok=ok, blockedword=blockedword_instance)
        return UpdateBlockedWord(ok=ok, blockedword=None)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_blockedword = CreateBlockedWord.Field()
    update_blockedword = UpdateBlockedWord.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)