from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.pagination import PageNumberPagination




class InvoiceList(APIView):
    def get(self, request, format=None):

        references = request.query_params.getlist('reference')
        vendors = request.query_params.getlist('vendor')
        patterns = request.query_params.getlist('pattern')
        open = request.query_params.get('open')
        group = request.query_params.get('group')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        invoices = Invoice.objects.all()
        if references:
            invoices = invoices.filter(reference__in=references)
        if vendors:
            invoices = invoices.filter(vendor__in=vendors)

        if patterns:
            invoices = invoices.filter(pattern__in=patterns)
        if open:
            invoices = invoices.filter(open__in=open)
        if group:
            invoices = invoices.filter(group__in=group)
        if start_date:
            invoices = invoices.filter(date__gte=start_date)
        if end_date:
            invoices = invoices.filter(date__lte=end_date)

        paginator = PageNumberPagination()
        paginated_invoices = paginator.paginate_queryset(invoices, request)
        serializer = InvoiceSerializer(paginated_invoices, many=True)
        return paginator.get_paginated_response(serializer.data)

class KPIsList(APIView):
    def get(self, request, format=None):
       # non_unique_invoices_count = Invoice.objects.exclude(pattern='unique').count()
       # non_unique_total_value = Invoice.objects.exclude(pattern='unique').aggregate(total_value=Invoice.Sum('value'))['total_value']
        return Response({'Total similar invoices': 15 , 'Total open similar invoices': 10, 'Total value of similar invoices': 10000, 'Total value of open similar invoices': 5000})