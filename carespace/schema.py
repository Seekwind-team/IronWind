import graphene
from graphene_django import DjangoObjectType

from carespace.models import CareSpace


class CareSpaceType(DjangoObjectType):
    class Meta:
        model = CareSpace
        description = 'This Type contains a singular CareSpace-Item posted'


class Query(graphene.AbstractType):
    get_care_space_items = graphene.List(CareSpaceType)
    get_care_space_item = graphene.Field(CareSpaceType, care_space_item_id=graphene.Int())

    def resolve_get_care_space_items(self, info, **kwargs):
        return list(CareSpace.objects.all())

    def resolve_get_care_space_item(self, info, care_space_item_id):
        return CareSpace.objects.filter(pk=care_space_item_id).get()
