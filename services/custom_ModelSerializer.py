from rest_framework import serializers
from services.reshape_error_messages import reshape_error_message
from rest_framework.exceptions import ValidationError


class CustomModelSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        try:
            is_valid = super(CustomModelSerializer, self).is_valid(raise_exception)
            self._errors = reshape_error_message(self._errors)
            return is_valid
        except ValidationError as e:
            e.detail = {"details": reshape_error_message(e.detail)}
            raise e


class DynamicSerializer(CustomModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = tuple(kwargs["context"]["request"].data.keys())
        super(DynamicSerializer, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
