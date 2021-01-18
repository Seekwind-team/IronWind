import graphene
from graphene_django import DjangoObjectType

from carespace.models import CareSpace, ArticleRead


class CareSpaceType(DjangoObjectType):
    class Meta:
        model = CareSpace
        description = 'This Type contains a singular CareSpace-Item posted'


class Query(graphene.AbstractType):
    get_care_space_items = graphene.List(
        CareSpaceType, description="returns alls Care Space Items"
    )
    get_care_space_item = graphene.Field(
        CareSpaceType,
        care_space_item_id=graphene.Int(
            description="ID of Care Space Item"
        ),
        description="returns Care Space Item with given ID"
    )

    def resolve_get_care_space_items(self, info, **kwargs):
        return list(CareSpace.objects.all())

    def resolve_get_care_space_item(self, info, care_space_item_id):
        article = CareSpace.objects.filter(pk=care_space_item_id).get()
        user = info.context.user
        if not ArticleRead.objects.filter(user=user, article=article):
            badges = user.get_badges()
            badges.articles_read += 1
            num_badges = badges.articles_read
            a = ArticleRead(user=user, article=article)
            a.save()
            if num_badges > 2:
                user.get_badges().top_vorbereitet = 2
            elif num_badges > 0:
                user.get_badges().top_vorbereitet = 1
            badges.save()
        return article
