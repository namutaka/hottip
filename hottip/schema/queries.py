import logging
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import models as auth_models
from graphene_django.filter import DjangoFilterConnectionField
from hottip.models import Channel, Tip, Distributor
from graphql_relay.node.node import from_global_id

LOGGER = logging.getLogger(__name__)

class UserNode(DjangoObjectType):
    class Meta:
        model = auth_models.User
        exclude_fields = ('password')


class ChannelNode(DjangoObjectType):
    class Meta:
        model = Channel
        filter_fields = (
            'name', 'description')
        only_fields = (
            'name', 'description',
            'created_at', 'updated_at',)
        interfaces = (graphene.relay.Node, )

    raw_id = graphene.Int()

    @staticmethod
    def resolve_raw_id(data, info):
        return data.id


class TipNode(DjangoObjectType):
    class Meta:
        model = Tip
        filter_fields = (
            'channel',
            'title', 'text', 'enable')
        only_fields = (
            'title', 'text', 'enable',
            'created_at', 'updated_at')
        interfaces = (graphene.relay.Node, )


class KeyValue(graphene.ObjectType):
    key = graphene.String(required=True)
    value = graphene.String()


class DistributorNode(DjangoObjectType):
    class Meta:
        model = Distributor
        filter_fields = (
            'channel', 'type')
        only_fields = (
            'schedule', 'type',
            'attribute', 'tips_count',
            'channel', 'created_at', 'updated_at')

    attribute = graphene.List(graphene.NonNull(KeyValue))

    @staticmethod
    def resolve_attribute(data, info):
        return [KeyValue(k, v) for k,v in data.attribute.items()]


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode)
    allChannels = DjangoFilterConnectionField(ChannelNode)
    allTips = DjangoFilterConnectionField(TipNode)
    distributors = graphene.List(DistributorNode)

    def resolve_me(self, info):
        return info.context.user

    def resolve_distributors(self, info, **kwargs):
        return Distributor.objects.all()

