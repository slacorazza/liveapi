from django.urls import path
from . import views

urlpatterns = [
    path("cases/", views.CaseListCreate.as_view(), name="case-list-create"),
    path("activities/", views.activityListCreate.as_view(), name="activity-list-create"),
    path("cases/<int:id>/", views.CaseRetrieveUpdateDestroy.as_view(), name="case-retrieve-update-destroy"),
    path("activities/<int:id>/", views.ActivityRetrieveUpdateDestroy.as_view(), name="activity-retrieve-update-destroy"),
    # Custom view for listing Activity objects with optional filtering and pagination
    path("activity-list/", views.ActivityList.as_view(), name="activity-list"),
    path('distinct-names/', views.ActivityNamesList.as_view(), name='distinct-names-list'),
    path('distinct-cases/', views.ActivityCaseList.as_view(), name='distinct-cases-list'),

]