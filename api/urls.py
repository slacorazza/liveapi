from django.urls import path
from . import views

"""
URL configuration for the API.

This module defines the URL patterns for the API endpoints, mapping them to the corresponding views.

Endpoints:
    - /invoices/ : Retrieve a list of invoices (InvoiceList view)
    - /kpis/ : Retrieve KPIs (KPIsList view)
"""

urlpatterns = [
    path("invoices/", views.InvoiceList.as_view(), name="invoice-list"),
    path("kpis/", views.KPIsList.as_view(), name="kpis-list"),
]