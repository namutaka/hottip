import logging
import graphene
from hottip.models import Channel, Tip, Distributor
from graphql_relay.node.node import from_global_id
from . import model_mutations, queries

LOGGER = logging.getLogger(__name__)


class CreateChannel(model_mutations.CreateMutation,
                    model=Channel,
                    field_name='channel',
                    object_type=queries.ChannelNode):

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()


class UpdateChannel(model_mutations.UpdateMutation,
                    model=Channel,
                    field_name='channel',
                    object_type=queries.ChannelNode):

    class Arguments:
        name = graphene.String()
        description = graphene.String()


class DeleteChannel(model_mutations.DeleteMutation,
                    model=Channel):
    pass


class CreateTip(model_mutations.CreateMutation,
                model=Tip,
                field_name='tip',
                object_type=queries.TipNode):

    class Arguments:
        channel_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        text = graphene.String()
        enable = graphene.Boolean(default_value=True)

    @classmethod
    def convert_fields(cls, fields):
        if 'channel_id' in fields:
            channel_id = from_global_id(fields.pop('channel_id'))[1]
            fields['channel'] = Channel.objects.get(id=channel_id)

        return fields


class UpdateTip(model_mutations.UpdateMutation,
                model=Tip,
                field_name='tip',
                object_type=queries.TipNode):

    class Arguments:
        title = graphene.String()
        text = graphene.String()
        enable = graphene.Boolean()


class DeleteTip(model_mutations.DeleteMutation,
                model=Tip):
    pass


class KeyValueInput(graphene.InputObjectType):
    key = graphene.String()
    value = graphene.String()

class CreateDistributor(model_mutations.CreateMutation,
                        model=Distributor,
                        field_name='distributor',
                        object_type=queries.DistributorNode):

    class Arguments:
        channel_id = graphene.ID(required=True)
        type = graphene.String(required=True)
        schedule = graphene.String()
        attribute = graphene.NonNull(graphene.List(graphene.NonNull(KeyValueInput)))
        tips_count = graphene.Int()

    @classmethod
    def convert_fields(cls, fields):
        if 'channel_id' in fields:
            channel_id = from_global_id(fields.pop('channel_id'))[1]
            fields['channel'] = Channel.objects.get(id=channel_id)

        if 'attribute' in fields:
            keyValueList = fields.pop('attribute')
            fields['attribute'] = dict((item['key'], item['value']) for item in keyValueList)

        return fields


class UpdateDistributor(model_mutations.UpdateMutation,
                        model=Distributor,
                        field_name='distributor',
                        object_type=queries.DistributorNode):

    class Arguments:
        type = graphene.String()
        schedule = graphene.String()
        tips_count = graphene.Int()
        attribute = graphene.List(graphene.NonNull(KeyValueInput))

    @classmethod
    def convert_fields(cls, fields):
        if 'attribute' in fields:
            keyValueList = fields.pop('attribute')
            fields['attribute'] = dict((item['key'], item['value']) for item in keyValueList)

        return fields

class DeleteDistributor(model_mutations.DeleteMutation,
                        model=Distributor):
    pass



class Mutation:
    create_channel = CreateChannel.Field()
    update_channel = UpdateChannel.Field()
    delete_channel = DeleteChannel.Field()

    create_tip = CreateTip.Field()
    update_tip = UpdateTip.Field()
    delete_tip = DeleteTip.Field()

    create_distributor = CreateDistributor.Field()
    update_distributor = UpdateDistributor.Field()
    delete_distributor = DeleteDistributor.Field()

