from django.urls import path
"""
URL configuration for the API.
This module defines the URL patterns for the API endpoints and maps them to the corresponding views.
Endpoints:
- cases/ : List and create cases.
- activities/ : List and create activities.
- cases/<int:id>/ : Retrieve, update, and destroy a specific case by ID.
- activities/<int:id>/ : Retrieve, update, and destroy a specific activity by ID.
- activity-list/ : List all activities.
- meta-data/ : Retrieve distinct activity data.
- variants/ : List all variants.
- KPI/ : List all KPIs.
- nopag/ : List all activities without pagination.
- avg-time-pair/ : Retrieve average time between activity pairs.
"""
from . import views

urlpatterns = [
    path("cases/", views.CaseListCreate.as_view(), name="case-list-create"),
    path("activities/", views.activityListCreate.as_view(), name="activity-list-create"),
    path("cases/<int:id>/", views.CaseRetrieveUpdateDestroy.as_view(), name="case-retrieve-update-destroy"),
    path("activities/<int:id>/", views.ActivityRetrieveUpdateDestroy.as_view(), name="activity-retrieve-update-destroy"),
    path("activity-list/", views.ActivityList.as_view(), name="activity-list"),
    path('meta-data/', views.DistinctActivityData.as_view(), name='distinct-activity-data'),
    path('variants/', views.VariantList.as_view(), name='variant-list'),
    path('KPI/', views.KPIList.as_view(), name='KPI'),
    path("nopag/", views.ActivityListNoPag.as_view(), name="activity-list-nopag"),
    path("avg-time-pair/", views.ActivityPairTime.as_view(), name="avg-time-list"),

]