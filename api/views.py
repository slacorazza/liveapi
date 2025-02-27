from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Case, Activity, Variant
from .serializers import CaseSerializer, ActivitySerializer, VariantSerializer
from rest_framework.pagination import PageNumberPagination


# View for listing and creating Case objects
class CaseListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of cases or create new
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

# View for listing and creating Activity objects
class activityListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of activities or create new
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

# View for retrieving, updating, and destroying Case objects
class CaseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete case
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    lookup_field = 'id'

# View for retrieving, updating, and destroying Activity objects
class ActivityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete activity
    """
    queryset = Activity.objects.all()

# Custom view for listing Activity objects with optional filtering and pagination
class ActivityList(APIView):
    """
    API view to retrieve list of activities with optional filtering by case IDs and names.
    Supports pagination.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list activities with optional filtering and pagination
        """
        case_ids = request.query_params.getlist('case')
        names = request.query_params.getlist('name')

        if case_ids and names:
            activities = Activity.objects.filter(case__id__in=case_ids, name__in=names)
        elif case_ids:
            activities = Activity.objects.filter(case__id__in=case_ids)
        elif names:
            activities = Activity.objects.filter(name__in=names)
        else:
            activities = Activity.objects.all()

        activities = activities.order_by('timestamp')

        paginator = PageNumberPagination()
        paginated_activities = paginator.paginate_queryset(activities, request)
        serializer = ActivitySerializer(paginated_activities, many=True)
        return paginator.get_paginated_response(serializer.data)
    

# View for listing all distinct activity names and case IDs
class DistinctActivityData(APIView):
    """
    API view to retrieve a list of all distinct activity names and case IDs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.
        """
        distinct_names = Activity.objects.values_list('name', flat=True).distinct()
        distinct_cases = Activity.objects.values_list('case', flat=True).distinct()
        return Response({
            'distinct_names': distinct_names,
            'distinct_cases': distinct_cases,
            'attributes': ['CASE', 'TIMESTAMP', 'ACTIVIDAD']
        })
    
class VariantList(APIView):
    """
    API view to retrieve a list of all distinct activity names and case IDs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.
        """

        activities_param = request.query_params.getlist('activities')
        cases_param = request.query_params.getlist('cases')
        variants = Variant.objects.all()
        if activities_param:
            for param in activities_param:
                variants = Variant.objects.filter(activities__icontains=param)
                print(param)
            

        variants = variants.order_by('percentage').reverse()
        
        paginator = PageNumberPagination()
        paginated_activities = paginator.paginate_queryset(variants, request)
        serializer = VariantSerializer(paginated_activities, many=True)
        return paginator.get_paginated_response(serializer.data)

