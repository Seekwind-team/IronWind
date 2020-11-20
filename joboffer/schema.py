# define all Job-Offer related Queries and Mutations here
import graphene
from graphql_jwt.decorators import user_passes_test, login_required
from graphene_django import DjangoObjectType

from joboffer.models import JobOffer
from user.schema import is_company


class JobOfferType(DjangoObjectType):

    class Meta:
        model = JobOffer


# creates new Job offer
class PostJobOffer(graphene.Mutation):

    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        pass

    @user_passes_test(lambda user: is_company(user))  # only applicable for company accounts
    def mutate(self, info, **kwargs):
        job_offer = None
        return PostJobOffer(job_offer=job_offer)


class AlterJobOffer(graphene.Mutation):
    pass


class DeleteJobOffer(graphene.Mutation):
    pass


class Mutation(graphene.ObjectType):
    post_job_offer = PostJobOffer.Field()
    alter_job_offer = AlterJobOffer.Field()
    delete_job_offer = DeleteJobOffer.Field()


class Query(graphene.AbstractType):
    my_job_offers = graphene.Field(JobOfferType)

    def resolve_my_job_offers(self):
        pass
