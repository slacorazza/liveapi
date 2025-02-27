from django.urls import path
from . import views

urlpatterns = [
    path("cases/", views.CaseListCreate.as_view(), name="case-list-create"),
    path("activities/", views.activityListCreate.as_view(), name="activity-list-create"),
    path("cases/<int:id>/", views.CaseRetrieveUpdateDestroy.as_view(), name="case-retrieve-update-destroy"),
    path("activities/<int:id>/", views.ActivityRetrieveUpdateDestroy.as_view(), name="activity-retrieve-update-destroy"),
    # Custom view for listing Activity objects with optional filtering and pagination
    path("activity-list/", views.ActivityList.as_view(), name="activity-list"),
    path('meta-data/', views.DistinctActivityData.as_view(), name='distinct-activity-data'),
    path('variants/', views.VariantList.as_view(), name='variant-list'),
    path('KPI/', views.KPIList.as_view(), name='KPI'),
    path("nopag/", views.ActivityListNoPag.as_view(), name="activity-list-nopag"),

]