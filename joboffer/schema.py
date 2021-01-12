# define all Job-Offer related Queries and Mutations here
import os
import uuid

import graphene
from django.db.models import Model
from django.utils import timezone
from graphql import GraphQLError
from graphql_jwt.decorators import user_passes_test, login_required
from graphene_django import DjangoObjectType

from django.core.validators import validate_email

from joboffer.models import JobOffer, Tag, Image, Swipe, Bookmark
from user.models import CompanyData, UserData
from user.schema import Upload
f#rom recommenders.recommender import Recommender

class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        description = 'Meta Object to hold information for Image-Objects attached to Job Offers'
        # excludes model to avoid recursive query sets
        exclude_fields = ('model',)


class SwipeType(DjangoObjectType):
    class Meta:
        model = Swipe
        description = 'Meta Object to hold information for Swipes between User and Job Offers'

class BookmarkType(DjangoObjectType):
    class Meta:
        model = Bookmark
        description = 'Meta Object to hold information for Bookmarks from Users on Job Offers'


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        description = 'Meta Object to hold Tag information'


class JobOfferType(DjangoObjectType):
    class Meta:
        model = JobOffer
        description = 'This Type contains a singular Job offer posted'
        convert_choices_to_enum = False

    created_at = graphene.DateTime(name='createdAt')
    must_have = graphene.String(name='mustHave')
    company_logo = graphene.String()
    images = graphene.List(graphene.String)
    nice_have = graphene.String(name='niceHave')

    def resolve_company_logo(self, info):
        return CompanyData.objects.filter(belongs_to=self.owner).get().company_picture.url

    def resolve_images(self, info):
        try:
            return Image.objects.filter(model=self).all()
        except Exception:
            return None


# creates new Job offer
class CreateJobOffer(graphene.Mutation):
    ok = graphene.Boolean(description="Will return on successful creation")
    job_offer = graphene.Field(JobOfferType, description="returns created joboffer")

    class Arguments:
        # cohooyo requirements
        job_type = graphene.String(required=True, description="'Vollzeit','Teilzeit','Ausbildung'")
        job_title = graphene.String(required=True, description="Name (Title) of the Job offered")
        location = graphene.String(description="Location of Job offer")
        description = graphene.String(description="description of the Job offered")
        highlights = graphene.String(description="Highlights of the Job Offered (eg. Homeoffice)")
        must_have = graphene.String(description="Must-haves for the job offered, eg Drivers License")
        nice_have = graphene.String(description="Conditions that arent required but would be nice to have")
        public_email = graphene.String(description="publicly visible email address")
        hashtags = graphene.List(graphene.String, description="Tags to describe Joboffer")

        # not relevant for Recommenders
        pay_per_year = graphene.List(graphene.String, description="Zu erwartendes Gehalt und des einzelnen Ausbildungsjahren")
        pay_per_hour = graphene.Int(description="Stundenlohn")
        city = graphene.String(description="Ort des Jobangebots")
        start_date = graphene.Date(description="Datum des ersten Arbeitstages")
        trade = graphene.String(description="Jobkategorie")

    @login_required
    @user_passes_test(lambda user: user.is_company)  # only applicable for company accounts
    def mutate(self, info,
               job_title,
               job_type=None,
               location=None,
               description=None,
               highlights=None,
               must_have=None,
               nice_have=None,
               public_email=None,
               hashtags=[],
               pay_per_year=None,
               pay_per_hour=None,
               city=None,
               start_date=None,
               trade=None
               ):
        job_object = JobOffer(owner=info.context.user)
        job_object.created_at = timezone.now()
        job_object.job_type = job_type
        job_object.job_title = job_title
        job_object.location = location
        job_object.description = description
        job_object.highlights = highlights
        job_object.must_have = must_have
        job_object.nice_have = nice_have
        job_object.public_email = public_email

        job_object.pay_per_year = pay_per_year
        job_object.pay_per_hour = pay_per_hour
        job_object.city = city
        job_object.start_date = start_date
        job_object.trade = trade

        job_object.save()

        # add existing Tag or create and add new one if hashtags is not empty
        if hashtags:
            for tag in hashtags:
                if Tag.objects.filter(name=tag).exists():
                    new_tag = Tag.objects.filter(name=tag).first()
                else:
                    new_tag = Tag(name=tag)
                    new_tag.save()

                job_object.hashtags.add(new_tag)

        return CreateJobOffer(job_offer=job_object, ok=True)


class AlterJobOffer(graphene.Mutation):
    ok = graphene.Boolean(description="returns true on successful creation")
    job_offer = graphene.Field(JobOfferType, description="returns altered job offer object")

    class Arguments:
        job_id = graphene.Int(required=True, description="ID of Job to be altered")
        job_type = graphene.String(description="'Vollzeit','Teilzeit','Ausbildung'")
        job_title = graphene.String(description="Name (Title) of the Job offered")
        location = graphene.String(description="Location of Job offer")
        description = graphene.String(description="description of the Job offered")
        highlights = graphene.String(description="Highlights of the Job Offered (eg. Homeoffice)")
        must_have = graphene.String(description="Must-haves for the job offered, eg Drivers License")
        nice_have = graphene.String(description="Conditions that arent required but would be nice to have")
        public_email = graphene.String(description="publicly visible email address")
        is_active = graphene.Boolean(description="Boolean, set to true will deactivate the public job offer")

        add_hashtags = graphene.List(graphene.String, description="Tags to describe Joboffer")
        remove_hashtags = graphene.List(graphene.String, description="Tags that should be removed")

        pay_per_year = graphene.List(graphene.String, description="Zu erwartendes Gehalt und des einzelnen Ausbildungsjahren")
        pay_per_hour = graphene.Int(description="Stundenlohn")
        city = graphene.String(description="Ort des Jobangebots")
        start_date = graphene.Date(description="Datum des ersten Arbeitstages, nutzt iso8601-Format (eg. 2006-01-02)")
        trade = graphene.String(description="Jobkategorie")

    @user_passes_test(lambda user: user.is_company)
    def mutate(self, info, job_id,
               job_title=None,
               job_type=None,
               location=None,
               description=None,
               highlights=None,
               must_have=None,
               nice_have=None,
               public_email=None,
               is_active=True,
               add_hashtags=[],
               remove_hashtags=[],
               pay_per_year=None,
               pay_per_hour=None,
               city=None,
               start_date=None,
               trade=None
               ):
        try:
            job_object = JobOffer.objects.filter(pk=job_id).get()
        except Exception:
            raise GraphQLError('Cannot reference Object')
        if job_object.owner == info.context.user:
            job_object.job_type = job_type or job_object.job_type
            job_object.job_title = job_title or job_object.job_title
            job_object.location = location or job_object.location
            job_object.description = description or job_object.description
            job_object.highlights = highlights or job_object.highlights
            job_object.must_have = must_have or job_object.must_have
            job_object.nice_have = nice_have or job_object.nice_have
            job_object.public_email = public_email or job_object.public_email
            job_object.is_active = is_active or job_object.is_active
            job_object.last_modified = timezone.now()

            job_object.pay_per_year = pay_per_year or job_object.pay_per_year
            job_object.pay_per_hour = pay_per_hour or job_object.pay_per_hour
            job_object.city = city or job_object.city
            job_object.start_date = start_date or job_object.start_date
            job_object.trade = trade or job_object.trade

            # add existing Tag or create and add new one
            for tag in add_hashtags:
                if Tag.objects.filter(name=tag).exists():
                    new_tag = Tag.objects.filter(name=tag).first()
                else:
                    new_tag = Tag(name=tag)
                    new_tag.save()

                job_object.hashtags.add(new_tag)

            # remove Tag from job offer
            for tag in remove_hashtags:
                if Tag.objects.filter(name=tag).exists():
                    tag = Tag.objects.filter(name=tag).get()
                    job_object.hashtags.remove(tag)

            job_object.save()
        else:
            raise GraphQLError('User does not own this JobOffer, aborting')
        return AlterJobOffer(job_offer=job_object, ok=True)


class DeleteJobOffer(graphene.Mutation):
    ok = graphene.Boolean(description="Returns True on successful operation")

    class Arguments:
        job_ID = graphene.Int(required=True,description="ID of Job to be deleted")

    @login_required
    def mutate(self, info, **kwargs):
        # checks if user owns joboffer
        user_job_offers = JobOffer.objects.filter(owner=info.context.user)
        job_offer = JobOffer.objects.filter(pk=kwargs['job_ID']).get()

        if job_offer in user_job_offers:
            job_offer.is_deleted = True
            job_offer.save()
            return DeleteJobOffer(ok=True)
        else:
            raise GraphQLError("User has no Job with id: ", kwargs['job_ID'])

        return DeleteJobOffer(ok=False)


class AddImage(graphene.Mutation):
    ok = graphene.Boolean(description="returns true on successful operation")
    image = graphene.Field(ImageType, description="Returns Image Object with metadata")

    class Arguments:
        job_offer_id = graphene.Int(required=True, description="ID of Job-Offer Image is being applied to")
        description = graphene.String(description="description for image")
        file_in = Upload(required=True, description="Uploaded File")

    @user_passes_test(lambda user: user.is_company)
    def mutate(self, info, file_in, description=None, **kwargs):
        c_user = info.context.user
        try:
            job = JobOffer.objects.filter(pk=kwargs['job_offer_id']).get()
        except Exception as e:  # or
            raise GraphQLError('Job does not Exist', e)
        if job.owner.id is not c_user.id:
            raise GraphQLError('User does not Own this Job')

        if len(Image.objects.filter(model=job).all()) > 4:
            raise GraphQLError("can't upload mora than 5 Images per JobOffer")

        if file_in.content_type not in ['image/jpg', 'image/jpeg', "image/png"]:
            raise GraphQLError("Provided invalid file format")

        extension = os.path.splitext(file_in.name)[1]
        file_in.name = "" + str(c_user.pk) + "_" + str(job.pk) + "_" + str(uuid.uuid4()) + extension

        image = Image(image=file_in, model=job)
        image.description = description
        image.save()

        image.width = image.image.width
        image.height = image.image.height
        image.save()

        return AddImage(ok=True, image=image)


class DeleteImage(graphene.Mutation):
    ok = graphene.Boolean(description="returns true on successful operation")
    joboffer = graphene.Field(JobOfferType, description="returns altered job-offer object")

    class Arguments:
        picture_ID = graphene.Int(required=True, description="ID of Picture to be deleted")
        job_ID = graphene.Int(required=True, description="ID of Picture to be deleted")

    @login_required
    def mutate(self, info, **kwargs):
        try:
            job = JobOffer.objects.filter(pk=kwargs['job_ID']).get()
        except Exception:
            raise GraphQLError('can\'t find Job with ID' + str(kwargs['job_ID']))
        # check ownership
        if job.owner.id is not info.context.user.pk:
            raise GraphQLError('Current user doesn\'t match ' + str(job) + '\'s owner')
        try:
            picture = job.image_set.filter(pk=kwargs['picture_ID']).get()
        except Exception:
            raise GraphQLError("can't Query Picture-ID '" + str(kwargs['picture_ID']) + " on job " + str(job))

        try:
            picture.image.storage.delete(picture.image.name)
        except Exception:
            print("WARNING: COULD NOT DELETE REFERENCED IMAGE FROM LOCAL STORAGE")
        # finally delete picture from database
        picture.delete()

        return DeleteImage(ok=True, joboffer=job)


# used to store like or dislike from user on joboffer
class SaveSwipe(graphene.Mutation):
    ok = graphene.Boolean()
    swipe = graphene.Field(SwipeType, description="returns new swipe")

    class Arguments:
        job_id = graphene.Int(required=True, description="ID of swiped job")
        like = graphene.Boolean(required=True, description="saves Like(true) or Dislike(false) between User and given job offer")
        reset = graphene.Boolean(description="set to true to reset swipe")

    @login_required
    def mutate(self, info, **kwargs):
        try:
            job = JobOffer.objects.filter(pk=kwargs['job_id']).get()
        except Exception:
            raise GraphQLError("can\'t find Job with ID {}".format(kwargs['job_id']))

        if not Swipe.objects.filter(candidate=info.context.user, job_offer=job).exists():
            # initial swipe
            swipe = Swipe(candidate=info.context.user, job_offer=job)
            swipe.liked = kwargs['like']
            swipe.save()
        elif Swipe.objects.filter(candidate=info.context.user, job_offer=job).get().liked != kwargs['like']:
            # alter like attribute
            swipe = Swipe.objects.filter(candidate=info.context.user, job_offer=job).get()
            swipe.liked = kwargs['like']
            swipe.save()
        else:
            raise GraphQLError("this joboffer is already {} by user".format('liked' if kwargs['like'] else 'disliked'))

        return SaveSwipe(ok=True, swipe=swipe)


# used to store joboffer for user as bookmarks
class SaveBookmark(graphene.Mutation):
    ok = graphene.Boolean()
    bookmark = graphene.Field(BookmarkType, description="returns new Bookmark")

    class Arguments:
        job_id = graphene.Int(required=True, description="ID of job to be bookmarked")

    @login_required
    def mutate(self, info, **kwargs):
        try:
            job = JobOffer.objects.filter(pk=kwargs['job_id']).get()
        except Exception:
            raise GraphQLError("can\'t find Job with ID {}".format(kwargs['job_id']))

        if not Bookmark.objects.filter(candidate=info.context.user, job_offer=job).exists():
            bookmark = Bookmark(candidate=info.context.user, job_offer=job)
            bookmark.save()
        else:
            raise GraphQLError("this bookmark is already set")

        return SaveBookmark(ok=True, bookmark=bookmark)


class DeleteBookmark(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        bookmark_id = graphene.Int(required=True, description="id of Bookmark to be deleted")

    @login_required
    def mutate(self, info, bookmark_id):
        bookmark = Bookmark.objects.filter(pk=bookmark_id).get()
        if info.context.user == bookmark.candidate:
            bookmark.delete()
        else:
            raise Exception("bookmark with id {} is not owned by User.".format(bookmark_id))

        return DeleteBookmark(ok=True)


class EndSearch(graphene.Mutation):

    ok = graphene.Boolean()

    class Arguments:
        pass

    @user_passes_test(lambda u: u.is_authenticated and not u.is_company)
    def mutate(self, info):
        userdata = info.context.user.get_data()
        userdata.looking = False
        userdata.save()
        JobOffer.objects.filter(swipe__candidate=info.context.user).all().delete()
        return EndSearch(ok=True)


class ReactivateSearch(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        pass

    @user_passes_test(lambda u: u.is_authenticated and not u.is_company)
    def mutate(self, info):
        userdata = info.context.user.get_data()
        userdata.looking = True
        userdata.save()
        return ReactivateSearch(True)


class Mutation(graphene.ObjectType):
    create_job_offer = CreateJobOffer.Field()
    alter_job_offer = AlterJobOffer.Field()
    delete_job_offer = DeleteJobOffer.Field()
    add_image = AddImage.Field()
    delete_image = DeleteImage.Field()
    save_swipe = SaveSwipe.Field()
    save_bookmark = SaveBookmark.Field()
    delete_bookmark = DeleteBookmark.Field()
    end_search = EndSearch.Field()
    reactivate_search = ReactivateSearch.Field()


class Query(graphene.AbstractType):
    job_offers = graphene.List(
        JobOfferType,
        description="returns list of all job-offers created by logged in company-user"
    )

    job_offer = graphene.Field(
        JobOfferType,
        job_Id=graphene.Int(
            description="ID of Job offer to be returned with this request"
        ),
        description="returns job offer with given ID"
    )

    bookmarks = graphene.List(
        BookmarkType,
        description="returns list of Bookmarks for logged in user"
    )

    swipes = graphene.List(
        SwipeType,
        description="returns list of Swipes for logged in user"
    )

    candidates = graphene.List(
        SwipeType,
        description="returns list of Swipes for logged in company"
    )

    all_tags = graphene.List(
        TagType,
    )

    job_offer_tag_search = graphene.List(
        JobOfferType,
        tag_names = graphene.List(
            graphene.String,
            description="tagnames to search for in joboffers"
        ),
        description="returns all joboffers that contain given tags"
    )

    @user_passes_test(lambda user: user.is_company)
    def resolve_job_offers(self, info):
        return list(JobOffer.objects.filter(owner=info.context.user, is_deleted=False))

    @login_required
    def resolve_job_offer(self, info, job_Id):
        if JobOffer.objects.filter(pk=job_Id).get().is_deleted:
            raise GraphQLError("this Joboffer is deleted")
        else:
            return JobOffer.objects.filter(pk=job_Id).get()

    @login_required
    def resolve_bookmarks(self, info):
        return list(Bookmark.objects.filter(candidate=info.context.user))

    @login_required
    def resolve_swipes(self, info):
        return list(Swipe.objects.filter(candidate=info.context.user))

    @user_passes_test(lambda user: user.is_company)
    def resolve_candidates(self, info):
        jobs = list(JobOffer.objects.filter(owner=info.context.user, is_deleted=False))
        swipes = []
        for job in jobs:
            query_set = Swipe.objects.filter(job_offer=job, liked=True)
            for swipe in query_set:
                swipes.append(swipe)

        return swipes

    # returns all tags that got a reference to a job offer
    @login_required
    def resolve_all_tags(self, info):
        all_tags = list(Tag.objects.all())
        active_tags = []
        for tag in all_tags:
            if tag.joboffer_set.all().first():
                active_tags.append(tag)

        return active_tags

    @login_required
    def resolve_job_offer_tag_search(self, info, tag_names):
        jobs = []
        
        # if not working change to tag_names.first()
        if not tag_names:
            # this is a copy of recommenders/schema.py. import is not possible because of circular imports. 
            #user_id = info.context.user.id
            #r = Recommender()
            #return r.recommend(user_id)
            return JobOffer.objects.all()

        for name in tag_names:
            tag = Tag.objects.filter(name=name).get()
            query_set = JobOffer.objects.filter(hashtags=tag)
            for job in query_set:
                jobs.append(job)

        return list(dict.fromkeys(jobs))
