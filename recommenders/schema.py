#Recommender interface
import graphene
import user.schema
from joboffer.models import JobOffer
from joboffer.schema import JobOfferType

class Query(graphene.ObjectType):
    my_recommendations = graphene.List(JobOfferType)

    def resolve_my_recommendations(self, info):
        # temp return value for frontend testing
        return JobOffer.objects.all()
