from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Case, Activity, Variant
from .serializers import CaseSerializer, ActivitySerializer, VariantSerializer
from rest_framework.pagination import PageNumberPagination
import json
from collections import defaultdict

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
    def get(self, request):
        """
        Handle GET request to list activities with optional filtering and pagination
        """
        try:
            case_ids = request.query_params.getlist('case')
            names = request.query_params.getlist('name')
            case_index = request.query_params.get('case_index')
            activities = Activity.objects.all()
            if case_index:
                activities = activities.filter(case_index=case_index)
            if case_ids:
                activities = activities.filter(case__id__in=case_ids)
            if names:
                activities = activities.filter(name__in=names)

            activities = activities.order_by('timestamp')

            paginator = PageNumberPagination()
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
        """
        distinct_names = Activity.objects.values_list('name', flat=True).distinct()
        distinct_cases = Activity.objects.values_list('case', flat=True).distinct()
        return Response({
            'distinct_names': distinct_names,
            'distinct_cases': distinct_cases,
            'attributes': ['CASE', 'TIMESTAMP', 'NAME', 'TPT']
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
                variants = variants.filter(activities__icontains=param)
                
            

        variants = variants.order_by('percentage').reverse()
        
        paginator = PageNumberPagination()
        paginated_activities = paginator.paginate_queryset(variants, request)
        serializer = VariantSerializer(paginated_activities, many=True)
        return paginator.get_paginated_response(serializer.data)

class KPIList(APIView):
    """
    API view to retrieve a list of all KPIs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.
        """

        kpi_data = {
            "CREATE": 15048.801916932907,
            "UPDATE": 47251.18092909535,
            "RESOLUTION ADD": 0.762589928057554,
            "RESOLUTION UPDATE": 7.890625,
            "RESOLVED": 2612.722891566265,
            "DELETE": 1989.448275862069,
            "RESTORE": 262133.72413793104,
            "SOLUTIONASSOCIATION": 20056.153846153848,
            "CLOSE": 686.4,
            "SLA_VIOLATION": 35208.23529411765,
            "REQ_CONVER": 15517.521739130434,
            "ATT_ADD": 10.333333333333334,
            "ADD_requestworklog": 57196.142857142855,
            "ADD_requesttask": 16817.333333333332,
            "COPY": 183335.82352941178,
            "DELETE_requesttask": 27.0,
            "REPLY": 163953.7142857143,
            "ADD_requestResponse": 67130.0,
            "FCR": 59986.0,
            "UPDATE_requestworklog": 604.0
        }

        formatted_kpi_data = [{"name": name, "avg_time": mean_time} for name, mean_time in kpi_data.items()]

        return Response(formatted_kpi_data)


class ActivityListNoPag(APIView):
    """
    API view to retrieve list of activities with optional filtering by case IDs and names.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list activities with optional filtering
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
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
class ActivityPairTime(APIView):

    def get_caseindex_list(self):
        activities = Activity.objects.all()
        case_index_list = []

        for activity in activities:
            if activity.case_index not in case_index_list:
                case_index_list.append(activity.case_index)
        return case_index_list
    
    def get_pair_list(self, case_index):
        activities = Activity.objects.filter(case_index=case_index).order_by('timestamp')
        activity_pairs = defaultdict(lambda: {'total_time': 0, 'occurrences': 0})

        for i in range(len(activities) - 1):
            current_activity = activities[i]
            next_activity = activities[i + 1]
            pair = (current_activity.name, next_activity.name)
            time_diff = (next_activity.timestamp - current_activity.timestamp).total_seconds()

            activity_pairs[pair]['total_time'] += time_diff
            activity_pairs[pair]['occurrences'] += 1

        return activity_pairs

    def get_avg_time_list(self):
        case_index_list = self.get_caseindex_list()
        all_activity_pairs = defaultdict(lambda: {'total_time': 0, 'occurrences': 0})

        for case_index in case_index_list:
            activity_pairs = self.get_pair_list(case_index)
            for pair, data in activity_pairs.items():
                all_activity_pairs[pair]['total_time'] += data['total_time']
                all_activity_pairs[pair]['occurrences'] += data['occurrences']
        avg_time_list = []
        for pair, data in all_activity_pairs.items():
            avg_time_dict = {}

            average_time = data['total_time'] / data['occurrences']
            avg_time_dict['pair'] = pair
            avg_time_dict['average_time'] = average_time
            avg_time_dict['occurrences'] = data['occurrences']
            avg_time_list.append(avg_time_dict)

        return avg_time_list
    
    def get(self, request, format=None):
        avg_time_list = self.get_avg_time_list()
        return Response(avg_time_list)