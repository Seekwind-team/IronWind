#Recommender interface
import graphene
import user.schema

from graphql_jwt.decorators import login_required

from recommender import Recommender
from joboffer.models import JobOffer
from joboffer.schema import JobOfferType

RCMDR = Recommender.new()

class Query(graphene.ObjectType):
    my_recommendations = graphene.List(JobOfferType)

    # needs testing
    @login_required
    def resolve_my_recommendations(self, info):
        RCMDR.preprocessing()
        RCMDR.createBow()
        RCMDR.createSimilarityMatrix()
        
        user_id = info.context.user.id

        return RCMDR.recommend(Recommender, user_id)
