# define all Job-Offer related Queries and Mutations here
import graphene
from graphql_jwt.decorators import user_passes_test, login_required
from graphene_django import DjangoObjectType

from django.core.validators import validate_email

from joboffer.models import JobOffer
from user.schema import is_company


class JobOfferType(DjangoObjectType):

    class Meta:
        model = JobOffer


# creates new Job offer
class CreateJobOffer(graphene.Mutation):

    ok = graphene.Boolean()
    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        job_type = graphene.String()
        job_title = graphene.String(required=True)
        location = graphene.String()
        description = graphene.String()
        highlights = graphene.String()
        must_have = graphene.String()
        public_email = graphene.String()
        
    @user_passes_test(lambda user: user.is_company)  # only applicable for company accounts
    def mutate(self, info = None,
                job_type = None,
                job_title = None, 
                location = None, 
                description = None, 
                highlights = None, 
                must_have = None, 
                public_email = None):
        job_offer = JobOffer(owner=info.context.user)
        job_offer.job_type = job_type
        job_offer.job_title = job_title
        job_offer.public_email = public_email
        job_offer.description = description
        job_offer.highlights = highlights
        job_offer.must_have = must_have
        job_offer.save()
        return CreateJobOffer(job_offer=job_offer, ok=True)


class AlterJobOffer(graphene.Mutation):

    ok = graphene.Boolean()
    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        job_type = graphene.String()
        job_title = graphene.String()
        location = graphene.String()
        description = graphene.String()
        highlights = graphene.String()
        must_have = graphene.String()
        public_email = graphene.String()
        is_active = graphene.Boolean()

    @user_passes_test(lambda user: user.is_company)
    def mutate(self, info, **kwargs):
        job_object = JobOffer.objects.filter(pk=id).get()
        if job_object.owner is info.context.user:
            job_object.job_type = kwargs['job_type'] or job_object.job_type
            job_object.job_title = kwargs['job_title'] or job_object.job_title
            job_object.location = kwargs['location'] or job_object.location
            job_object.description = kwargs['description'] or job_object.description
            job_object.highlights = kwargs['highlights'] or job_object.highlights
            job_object.must_have = kwargs['must_have'] or job_object.must_have
            job_object.public_email = kwargs['public_email'] or job_object.public_email
            job_object.is_active = kwargs['is_active'] or job_object.is_active
            job_object.save()
        else:
            raise Exception('User does not own this JobOffer, aborting')
        return AlterJobOffer(job_object=job_object, ok=True)


class DeleteJobOffer(graphene.Mutation):

    ok = graphene.Boolean()

    class Arguments:
        # frontendseitige bestätigung reicht?
        #assured = graphene.Boolean(required = True, description = "Must provide assurance to delete Joboffer")
        job_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        # checks if user owns joboffer
        user_job_offers = JobOffer.objects.filter(owner=info.context.user).get()
        job_offer = JobOffer.objects.filter(pk=kwargs['job_id']).get()
        
        if job_offer in user_job_offers:
            job_offer.delete()
        else:
            raise Exception("User has no Job with id: ", kwargs['job_id'])


class Mutation(graphene.ObjectType):
    create_job_offer = CreateJobOffer.Field()
    alter_job_offer = AlterJobOffer.Field()
    delete_job_offer = DeleteJobOffer.Field()


class Query(graphene.AbstractType):
    job_offers = graphene.List(JobOfferType)
    job_offer = graphene.Field(JobOfferType, job_id=graphene.Int())

    @user_passes_test(lambda u: u.isCompany)
    def resolve_job_offers(self, info):
        return JobOffer.objects.filter(owner=info.context.user).get()

    @login_required
    def resolve_job_offer(self, info, job_id):
        return JobOffer.objects.filter(pk=job_id).get()
