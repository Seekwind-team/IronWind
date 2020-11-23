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

    ok = graphene.Boolean()
    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        job_title = graphene.String(required=True)
        location = graphene.String()
        email = graphene.String()
        description = graphene.String()
        highlights = graphene.String()
        must_have = graphene.String()

    @user_passes_test(lambda user: user.is_company)  # only applicable for company accounts
    def mutate(self, info, **kwargs):
        if kwargs['bar']:
            foo = kwargs['bar']
        job_offer = JobOffer(owner=info.context.user)
        job_offer.job_title = kwargs['job_title']
        job_offer.public_email = "123@123.eu"
        job_offer.description = kwargs['description']
        job_offer.highlights = kwargs['highlights']
        job_offer.must_have = kwargs['must_have']
        job_offer.save()
        return PostJobOffer(job_offer=job_offer, ok=True)


class AlterJobOffer(graphene.Mutation):

    ok = graphene.Boolean()
    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        job_offer = graphene.ID()
        job_title = graphene.String()
        description = graphene.String()
        location = graphene.String()
        email = graphene.String()
        highlights = graphene.String()
        must_have = graphene.String()
        is_active = graphene.Boolean()

    @user_passes_test(lambda user: user.is_company)
    def mutate(self, info, **kwargs):
        job_object = JobOffer.objects.filter(pk=id).get()
        if job_object.owner is info.context.user:
            job_object.job_title = kwargs['job_title'] or job_object.job_title
            job_object.description = kwargs['description'] or job_object.description
            job_object.location = kwargs['location'] or job_object.location
            job_object.public_email = kwargs['email'] or job_object.public_email
            job_object.highlights = kwargs['highlights'] or job_object.highlights
            job_object.must_have = kwargs['must_have'] or job_object.must_have
            job_object.is_active = kwargs['is_active'] or job_object.is_active
            job_object.save()
        else:
            raise Exception('User does not own this JobOffer, aborting')
        return AlterJobOffer(job_object=job_object, ok=True)


class Mutation(graphene.ObjectType):
    post_job_offer = PostJobOffer.Field()
    alter_job_offer = AlterJobOffer.Field()
    # delete_job_offer = DeleteJobOffer.Field()


class Query(graphene.AbstractType):
    job_offers = graphene.List(JobOfferType)
    job_offer = graphene.Field(JobOfferType, job_id=graphene.Int())

    def resolve_job_offers(self, info):
        return JobOffer.objects.filter(owner=info.context.user).get()

    def resolve_job_offer(self, info, job_id):
        return JobOffer.objects.filter(pk=job_id).get()
