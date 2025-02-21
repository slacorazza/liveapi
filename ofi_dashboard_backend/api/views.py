

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Case, Activity
from .serializers import CaseSerializer, ActivitySerializer
from rest_framework.pagination import PageNumberPagination

class CaseListCreate(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class activityListCreate(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class CaseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    lookup_field = 'id'

class ActivityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()

from rest_framework.pagination import PageNumberPagination

class ActivityList(APIView):
    def get(self, request, format=None):
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