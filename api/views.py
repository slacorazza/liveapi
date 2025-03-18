from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Case, Activity, Variant
from .serializers import CaseSerializer, ActivitySerializer, VariantSerializer
from rest_framework.pagination import PageNumberPagination
from collections import defaultdict

# View for listing and creating Case objects
class CaseListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of cases or create new.
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

# View for listing and creating Activity objects
class activityListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of activities or create new.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer



# Custom view for listing Activity objects with optional filtering and pagination
class ActivityList(APIView):
    """
    API view to retrieve list of activities with optional filtering by case IDs and names.
    Supports pagination.
    """
    def get(self, request):
        """
        Handle GET request to list activities with optional filtering and pagination.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The paginated list of activities.
        """
        try:
            case_ids = request.query_params.getlist('case')
            names = request.query_params.getlist('name')
            case_index = request.query_params.get('case_index')
            page_size = request.query_params.get('page_size', 100000)  # Default page size is 10 if not provided
            activities = Activity.objects.all()
            if case_index:
                activities = activities.filter(case_index=case_index)
            if case_ids:
                activities = activities.filter(case__id__in=case_ids)
            if names:
                activities = activities.filter(name__in=names)

            activities = activities.order_by('timestamp')

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            paginated_activities = paginator.paginate_queryset(activities, request)
            serializer = ActivitySerializer(paginated_activities, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# View for listing all distinct activity names and case IDs
class DistinctActivityData(APIView):
    """
    API view to retrieve a list of all distinct activity names and case IDs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.

        Args:
            request: The HTTP request object.
            format: The format of the response.

        Returns:
            Response: The list of distinct activity names and case IDs.
        """
        try:
            distinct_names = list(Activity.objects.values_list('name', flat=True).distinct())
            distinct_cases = list(Activity.objects.values_list('case', flat=True).distinct())
            distinct_types = list(Case.objects.values_list('type', flat=True).distinct())
            distinct_branches = list(Case.objects.values_list('branch', flat=True).distinct())
            distinct_ramos = list(Case.objects.values_list('ramo', flat=True).distinct())
            distinct_brockers = list(Case.objects.values_list('brocker', flat=True).distinct())
            distinct_clients = list(Case.objects.values_list('client', flat=True).distinct())
            distinct_creators = list(Case.objects.values_list('creator', flat=True).distinct())

            attributes = [
                {'name': 'case', 'type': 'number', 'distincts': distinct_cases},
                {'name': 'timestamp', 'type': 'date', 'distincts': []},  # Assuming no distinct values for timestamp
                {'name': 'name', 'type': 'str', 'distincts': distinct_names},
                {'name': 'tpt', 'type': 'number', 'distincts': []},  # Assuming no distinct values for tpt
                {'name': 'type', 'type': 'str', 'distincts': distinct_types},
                {'name': 'branch', 'type': 'str', 'distincts': distinct_branches},
                {'name': 'ramo', 'type': 'str', 'distincts': distinct_ramos},
                {'name': 'brocker', 'type': 'str', 'distincts': distinct_brockers},
                {'name': 'state', 'type': 'str', 'distincts': []},  # Assuming no distinct values for state
                {'name': 'client', 'type': 'str', 'distincts': distinct_clients},
                {'name': 'creator', 'type': 'str', 'distincts': distinct_creators},
            ]

            return Response({
                'attributes': attributes
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
class VariantList(APIView):
    """
    API view to retrieve a list of all distinct activity names and case IDs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.

        Args:
            request: The HTTP request object.
            format: The format of the response.

        Returns:
            Response: The paginated list of variants.
        """
        activities_param = request.query_params.getlist('activities')
        page_size = request.query_params.get('page_size', 100000)  # Default page size is 10 if not provided
        variants = Variant.objects.all()
        if activities_param:
            for param in activities_param:
                variants = variants.filter(activities__icontains=param)
                
        variants = variants.order_by('-percentage')
        
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_variants = paginator.paginate_queryset(variants, request)
        serializer = VariantSerializer(paginated_variants, many=True)
        return paginator.get_paginated_response(serializer.data)
