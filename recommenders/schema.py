#Recommender interface
import graphene
import user.schema

from graphql_jwt.decorators import login_required

from recommenders.recommender import Recommender
from joboffer.models import JobOffer
from joboffer.schema import JobOfferType

class Query(graphene.ObjectType):
    my_recommendations = graphene.List(JobOfferType)
    
    # needs testing
    @login_required
    def resolve_my_recommendations(self, info):
        user_id = info.context.user.id
        r = Recommender()
        return r.recommend(user_id)