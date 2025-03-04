from rest_framework import serializers
from .models import Case, Activity, Variant


## Serializer are used to convert complex data types, such as querysets and model instances, to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

class CaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Case model.

    This serializer converts Case instances to native Python datatypes
    that can be easily rendered into JSON, XML or other content types.

    Meta:
        model (Case): The model to be serialized.
        fields (str): All fields of the model.
    """
    class Meta:
        model = Case
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Activity model.

    This serializer converts Activity instances to native Python datatypes
    that can be easily rendered into JSON, XML or other content types.

    Meta:
        model (Activity): The model to be serialized.
        fields (list): The fields of the model to be serialized.
    """
    class Meta:
        model = Activity
        fields =  ['id','case', 'timestamp', 'name', 'case_index']	

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'activities', 'cases', 'number_cases', 'percentage', 'avg_time']
        