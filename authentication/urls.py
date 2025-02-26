from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('validate-token/', views.validate_token.as_view(), name='validate-token'),
]
