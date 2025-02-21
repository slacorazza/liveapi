from rest_framework import serializers
from .models import Case, Activity

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields =  ['id','case', 'timestamp', 'name', 'case_index']	
        