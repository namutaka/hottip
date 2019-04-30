import logging
import graphene
from django.core.exceptions import ValidationError
from graphql_relay.node.node import from_global_id

logger = logging.getLogger(__name__)


class ErrorType(graphene.ObjectType):
    field = graphene.String(required=True)
    messages = graphene.List(graphene.NonNull(graphene.String), required=True)

    @staticmethod
    def list_from_dict(error_dict):
        return [ErrorType(field=key, messages=value)
                for key, value in error_dict.items()]


class CreateMutation(graphene.Mutation):
    errors = graphene.List(graphene.NonNull(ErrorType), required=True)

    @classmethod
    def __init_subclass__(cls, model, field_name, object_type, **kwargs):
        cls.model = model
        cls.field_name = field_name
        setattr(cls, cls.field_name, graphene.Field(object_type))
        super().__init_subclass__(**kwargs)

    @classmethod
    def convert_fields(cls, fields):
        return fields

    @classmethod
    def mutate(cls, root, info, **fields):
        model_fields = cls.convert_fields(fields)
        obj = cls.model(**model_fields)

        try:
            obj.full_clean()
            obj.save()

            return cls(**{cls.field_name: obj}, errors=[])

        except ValidationError as e:
            return cls(
                errors=ErrorType.list_from_dict(e.message_dict))


class UpdateMutation(graphene.Mutation):
    errors = graphene.List(graphene.NonNull(ErrorType), required=True)

    class Arguments:
        pass

    @classmethod
    def __init_subclass__(cls, model, field_name, object_type, **kwargs):
        cls.model = model
        cls.field_name = field_name
        setattr(cls, cls.field_name, graphene.Field(object_type))

        args = getattr(cls, 'Arguments')
        setattr(args, 'id', graphene.ID(required=True))

        super().__init_subclass__(**kwargs)

    @classmethod
    def convert_fields(cls, fields):
        return fields

    @classmethod
    def mutate(cls, root, info, **fields):
        id = fields.pop('id')
        obj_id = from_global_id(id)[1]
        obj = cls.model.objects.get(pk=obj_id)

        model_fields = cls.convert_fields(fields)
        for key, value in model_fields.items():
            setattr(obj, key, value)

        try:
            obj.full_clean()
            obj.save(update_fields=model_fields.keys())
            return cls(**{cls.field_name: obj}, errors=[])

        except ValidationError as e:
            return cls(
                errors=ErrorType.list_from_dict(e.message_dict))


class DeleteMutation(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    class Arguments:
        pass

    @classmethod
    def __init_subclass__(cls, model, **kwargs):
        cls.model = model

        args = getattr(cls, 'Arguments')
        setattr(args, 'id', graphene.ID(required=True))

        super().__init_subclass__(**kwargs)


    @classmethod
    def mutate(cls, root, info, **fields):
        id = fields.pop('id')
        obj_id = from_global_id(id)[1]

        obj = cls.model.objects.get(pk=obj_id)
        ret = obj.delete()
        return cls(ok=(ret[0] > 0))

