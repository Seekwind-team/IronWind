# define all Job-Offer related Queries and Mutations here
import graphene
from django.utils import timezone
from graphql_jwt.decorators import user_passes_test, login_required
from graphene_django import DjangoObjectType

from django.core.validators import validate_email

from joboffer.models import JobOffer
from user.schema import is_company


class JobOfferType(DjangoObjectType):

    class Meta:
        model = JobOffer
        description = 'This Type contains a singular Joboffer posted'

    created_at = graphene.DateTime(name='created_at')
    must_have = graphene.String(name='must_have')
    # nice_have = graphene.String(name='nice_have') # not implemented!


# creates new Job offer
class CreateJobOffer(graphene.Mutation):

    ok = graphene.Boolean()
    job_offer = graphene.Field(JobOfferType)

    class Arguments:
        job_type = graphene.String(description="'Vollzeit','Teilzeit','Ausbildung'")
        job_title = graphene.String(required=True, description="Name (Title) of the Job offered")
        location = graphene.String(description="Location of Job offer")
        description = graphene.String(description="description of the Job offered")
        highlights = graphene.String(description="Highlights of the Job Offered (eg. Homeoffice)")
        must_have = graphene.String(description="Must-haves for the job offered, eg Drivers License")
        public_email = graphene.String(required=True, description="publicly visible email address")

    @login_required
    @user_passes_test(lambda user: user.is_company)  # only applicable for company accounts
    def mutate(self, info,
                job_type = None,
                job_title = None, 
                location = None, 
                description = None, 
                highlights = None, 
                must_have = None, 
                public_email = None):
        job_offer = JobOffer(owner=info.context.user)
        job_offer.created_at = timezone.now()
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
        job_type = graphene.String(description="'Vollzeit','Teilzeit','Ausbildung'")
        job_title = graphene.String(description="Name (Title) of the Job offered")
        location = graphene.String(description="Location of Job offer")
        description = graphene.String(description="description of the Job offered")
        highlights = graphene.String(description="Highlights of the Job Offered (eg. Homeoffice)")
        must_have = graphene.String(description="Must-haves for the job offered, eg Drivers License")
        public_email = graphene.String(description="publicly visible email address")
        is_active = graphene.Boolean(description="Boolean, set to true will deactivate the public job offer")

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
            job_object.last_modified = timezone.now()
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
            return DeleteJobOffer(ok=True)
        else:
            raise Exception("User has no Job with id: ", kwargs['job_id'])
        return DeleteJobOffer(ok=False)


class Mutation(graphene.ObjectType):
    create_job_offer = CreateJobOffer.Field()
    alter_job_offer = AlterJobOffer.Field()
    delete_job_offer = DeleteJobOffer.Field()


class Query(graphene.AbstractType):
    job_offers = graphene.List(JobOfferType)
    job_offer = graphene.Field(JobOfferType, job_id=graphene.Int())

    @user_passes_test(lambda user: user.is_company)
    def resolve_job_offers(self, info):
        return list(JobOffer.objects.filter(owner=info.context.user))

    @login_required
    def resolve_job_offer(self, info, job_id):
        return JobOffer.objects.filter(pk=job_id).get()
