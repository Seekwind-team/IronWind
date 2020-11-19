#Recommender interface
import graphene
import user.schema

class Query(graphene.ObjectType):
    def resolve_get_recommentations(self, user, jobs):
        #call function with user and jobs
        user = user
