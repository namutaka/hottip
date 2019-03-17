import json

from django.db import models
from django.core import exceptions

class JsonField(models.TextField):

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)


    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, str):
            try:
                return json.loads(value)

            except ValueError:
                raise exceptions.ValidationError(
                    "'%(value)s' is not valid JSON.",
                    code='invalid',
                    params={'value': value},
                )

        return value


    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, dict):
            return json.dumps(value)
        if isinstance(value, str):
            return value

        raise ValueError('JSONField value must be a dict or string')

