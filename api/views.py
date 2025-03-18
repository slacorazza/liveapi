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

# View for retrieving, updating, and destroying Case objects
class CaseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete case.
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    lookup_field = 'id'

# View for retrieving, updating, and destroying Activity objects
class ActivityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete activity.
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
        distinct_names = Activity.objects.values_list('name', flat=True).distinct()
        distinct_cases = Activity.objects.values_list('case', flat=True).distinct()
        attributes = ['CASE', 'TIMESTAMP', 'NAME', 'TPT', 'TYPE', 'BRANCH', 'RAMO', 'BROCKER', 'STATE', 'CLIENT', 'CREATOR']
        types = ['number', 'date', 'str', 'number', 'str', 'str', 'str', 'str', 'str', 'str', 'str']
        paired_attributes = [{'name': attr.lower(), 'type': typ} for attr, typ in zip(attributes, types)]
        
        return Response({
            'distinct_names': distinct_names,
            'distinct_cases': distinct_cases,
            'attributes': paired_attributes
        })
    
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

class KPIList(APIView):
    """
    API view to retrieve a list of all KPIs.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list all distinct activity names and case IDs.

        Args:
            request: The HTTP request object.
            format: The format of the response.

        Returns:
            Response: The list of KPIs.
        """
        kpi_data = {
    "Registro de compromiso": 1825.86,
    "Enviar a Revision suscripcion": 1842.504892367906,
    "Realizar devolucion desde suscripcion": 1880.6577595066803,
    "Validar info enviada": 1829.5865237366004,
    "Devolver caso a Comercial": 1790.7197549770292,
    "Ingresar tramite": 1830.4761904761904,
    "Registrar PO": 1779.9347471451877,
    "Enviar a emision": 1903.4285714285713,
    "Revision en emision": 1802.7457627118645,
    "Devolucion a comercial desde emision": 1759.109589041096,
    "Control de calidad documental": 1816.7763157894738,
    "Devolucion a emision de control de calidad": 1851.5131578947369,
    "Iniciar facturacion": 1836.0207612456747,
    "Generar Factura": 1795.9515570934257,
    "Contabilizar Factura": 1805.2941176470588,
    "Generar poliza": 1840.795847750865,
    "Enviar factura electronica": 1860.311418685121,
    "Respuesta SRI": 1726.712802768166,
    "Enviar poliza electronica": 1849.1003460207612,
    "Firma poliza electronica por parte del cliente": 1829.1695501730103,
    "Finalizar envio poliza y factura al cliente": 1811.9799777530588,
    "Finalizar proceso de emision": 1772.2837370242214,
    "Recepcion pago": 1880.9330628803245,
    "Aprobar solicitud en suscripcion local": 1808.7179487179487,
    "Enviar respuesta al area comercial": 1807.4358974358975,
    "Devolucion a emision": 1792.5,
    "Aceptar (ganado) por parte del Brocker": 1784.4705882352941,
    "Visado": 1787.6785714285713,
    "Devolucion a comercial (corregir informacion)": 1855.686274509804,
    "Devolucion a comercial desde visado": 1856.819012797075,
    "Devolucion al brocker del caso (Revision Brocker)": 1788.523489932886,
    "Devolucion a visado desde emision": 2013.2903225806451
}

        formatted_kpi_data = [{"name": name, "avg_time": mean_time} for name, mean_time in kpi_data.items()]

        return Response(formatted_kpi_data)


class ActivityListNoPag(APIView):
    """
    API view to retrieve list of activities with optional filtering by case IDs and names.
    """
    def get(self, request, format=None):
        """
        Handle GET request to list activities with optional filtering.

        Args:
            request: The HTTP request object.
            format: The format of the response.

        Returns:
            Response: The list of activities.
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
    """
    API view to retrieve the average time between pairs of activities.
    """
    def get_caseindex_list(self):
        """
        Retrieve a list of all distinct case indices.

        Returns:
            list: The list of distinct case indices.
        """
        activities = Activity.objects.all()
        case_index_list = []

        for activity in activities:
            if activity.case_index not in case_index_list:
                case_index_list.append(activity.case_index)
        return case_index_list
    
    def get_pair_list(self, case_index):
        """
        Retrieve a list of activity pairs and their total time and occurrences for a given case index.

        Args:
            case_index: The case index to filter activities by.

        Returns:
            defaultdict: The dictionary of activity pairs with their total time and occurrences.
        """
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
        """
        Retrieve a list of average times between activity pairs.

        Returns:
            list: The list of average times between activity pairs.
        """
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
        """
        Handle GET request to list the average time between pairs of activities.

        Args:
            request: The HTTP request object.
            format: The format of the response.

        Returns:
            Response: The list of average times between pairs of activities.
        """
        avg_time_list = self.get_avg_time_list()
        return Response(avg_time_list)