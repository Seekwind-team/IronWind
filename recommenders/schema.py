#Recommender interface
import graphene
import user.schema

from graphql_jwt.decorators import login_required

from recommenders.recommender import Recommender
from joboffer.models import JobOffer
from joboffer.schema import JobOfferType

class Query(graphene.ObjectType):
    my_recommendations = graphene.List(JobOfferType)
    
    def __init__():
        self.RCMDR = Recommender()
    
    # needs testing
    @login_required
    def resolve_my_recommendations(self, info):
        user_id = info.context.user.id

        return self.RCMDR.recommend(Recommender, user_id)
