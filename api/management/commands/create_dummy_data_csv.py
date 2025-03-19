import csv
from django.core.management.base import BaseCommand
from api.models import Case, Activity, Variant, Bill, Rework
from django.conf import settings
import os
from datetime import datetime
from collections import defaultdict
import random
from datetime import timedelta
from ..constants import NAMES, RAMOS, BRANCHES
import json
from django.utils import timezone

class Command(BaseCommand):
    """
    Django management command to add data to the database from a CSV file.
    """
    help = 'Add data to the database from CSV file'
    
    class Case:
        def __init__(self, case_id, case_type, last_timestamp, branch, ramo, brocker, state, client, creator, value, insurance):
            self.case_id = case_id
            self.type = case_type
            self.last_timestamp = last_timestamp
            self.branch = branch
            self.ramo = ramo
            self.brocker = brocker
            self.state = state
            self.client = client
            self.creator = creator
            self.value = value
            self.insurance = insurance

    cases_ids = []

    def new_case_id(self):
        case_id = random.randint(1, 10000)
        while case_id in self.cases_ids:
            case_id = random.randint(1, 10000)
        self.cases_ids.append(case_id)
        return case_id
    
    def write_in_file(self, case: Case, activity):
        """
        Write the data to the CSV file.

        Args:
            case_id (str): The ID of the case.
            activity (str): The activity.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        file_exists = os.path.isfile('data.csv')
        with open('data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Case ID', 'Activity', 'Timestamp', 'Case Type', 'Branch', 'Ramo', 'Brocker', 'Client', 'Creator', 'Value', 'Insurance', 'State'])
            writer.writerow([case.case_id, activity, case.last_timestamp, case.type, case.branch, case.ramo, case.brocker, case.client, case.creator, case.value, case.insurance, case.state])
        

        case2 = Case.objects.get(id=case.case_id)

        Activity.objects.create(case = case2, name=activity, timestamp=case.last_timestamp, case_index=case.case_id)

    def update_case(self, case: Case, activity):
        case.last_timestamp +=  timedelta(hours=random.expovariate(1/12))
        case.state = activity
        self.write_in_file(case, activity)

    def start(self):
        case_type = random.choice(['Renewal', 'Issuance', 'Policy onboarding'])
        case_id = self.new_case_id()
        initial_timestamp = timezone.make_aware(datetime(2025, 1, 1, 12, 0, 0) + timedelta(days=random.randint(1, 76), hours=random.randint(1, 24), minutes=random.randint(1, 60), seconds=random.randint(1, 60)))
        value = random.randint(10, 100)*100
        insurance = f"{random.randint(1, 100000):06d}"
        case = self.Case(case_id, case_type, initial_timestamp, branch=random.choice(BRANCHES), ramo=random.choice(RAMOS), brocker=random.choice(NAMES), state = 'Start', client =random.choice(NAMES), creator = random.choice(NAMES), value=value, insurance=insurance)


        Case.objects.create(id=case.case_id, type=case.type, avg_time=0, branch=case.branch, ramo=case.ramo, brocker=case.brocker, state=case.state, client=case.client, creator=case.creator, value=case.value, insurance=insurance)
        if case_type == 'Policy onboarding':
            self.ingresar_tramite(case)
        elif case_type == 'Renewal':
            rand_num = random.randint(1, 100)
            if rand_num <= 50:
                self.visado(case)
      
        self.registro_de_compromiso(case)

    def ingresar_tramite(self, case: Case):
        """
        Add a record of commitment to the database.

        Args:
            case_id (str): The ID of the case.
            initial_timestamp (datetime): The initial timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Ingresar tramite')
        
        self.registrar_PO(case)
    
    def registrar_PO(self, case: Case):
        """
        Add a record of commitment to the database.

        Args:
            case_id (str): The ID of the case.
            initial_timestamp (datetime): The initial timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Registrar PO')
        
        rand_num = random.randint(1, 100)
        if rand_num <= 10:
            self.update_case(case, 'Devolucion al brocker del caso (Revision Brocker)')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name = 'Registrar PO').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)
            
            self.registrar_PO(case)
        else:
            self.update_case(case, 'Enviar a emision')
            self.revision_emision(case)

    def registro_de_compromiso(self, case: Case):
        """
        Add a record of commitment to the database.

        Args:
            case_id (str): The ID of the case.
            initial_timestamp (datetime): The initial timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Registro de compromiso')
        self.enviar_revision_suscripcion(case)
    
    def enviar_revision_suscripcion(self, case: Case):
        """
        Add a subscription review to the database.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Enviar a Revisión suscripción')
        rand_num = random.randint(1, 100)
        if rand_num <= 50:
            self.validar_info_enviada(case)
        else:
            self.revision_suscripcion(case)
    
    def validar_info_enviada(self, case: Case):
        """
        Validate the information sent.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Validar info enviada')
        rand_num = random.randint(1, 100)
        if rand_num <= 10:
            self.update_case(case, 'Devolver caso a Comercial')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name = 'Enviar a Revisión suscripción').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.enviar_revision_suscripcion(case)
        else:
            self.revision_suscripcion(case)
    
    def revision_suscripcion(self, case: Case):
        """
        Add a subscription review to the database.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Revisión en suscripción')
        rand_num = random.randint(1, 50)
        if rand_num <= 10:
            self.update_case(case, 'Realizar devolucion desde suscripcion')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name = 'Enviar a Revisión suscripción').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.enviar_revision_suscripcion(case)
        elif rand_num <= 50:
            self.update_case(case, 'Enviar a suscripcion local')
            
        rand_num = random.randint(1, 100)
        if rand_num <= 10:
            self.update_case(case, 'Declinar solicitud en suscripcion')
        else:
            self.aprobar_suscripcion_local(case)

    def aprobar_suscripcion_local(self, case: Case):
        """
        Approve the local subscription.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Aprobar solicitud en suscripcion local')
        self.update_case(case, 'Enviar respuesta al area comercial')
        
        rand_num = random.randint(1, 100)
        if rand_num <= 33:
            self.update_case(case, 'Rechazar (perdida) por parte del Brocker')
        elif rand_num <= 66:
            self.update_case(case, 'Declinar por parte del Brocker')
        else:
            self.aceptar_brocker(case)

    def aceptar_brocker(self, case: Case):
        """
        Accept the broker.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Aceptar (ganado) por parte del Brocker')
        self.visado(case)

    def visado(self, case: Case):
        """
        Add a visa to the database.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Visado')
        
        rand_num = random.randint(1, 100)
        if rand_num <= 10:
            self.update_case(case, 'Devolucion a comercial desde visado')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name='Visado').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.visado(case)
        else:
            self.revision_emision(case)

            
    def revision_emision(self, case: Case):
        """
        Add an issuance review to the database.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Revisión en emisión')
        rand_num = random.randint(1, 100)
        if rand_num <= 10:
            self.update_case(case, 'Devolucion a comercial desde emisión')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name='Revisión en emisión').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.revision_emision(case)
        elif rand_num <= 20:
            self.update_case(case, 'Devolucion a visado desde emisión')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name='Visado').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.visado(case)
        elif rand_num <= 50:
            self.update_case(case, 'Control de calidad documental')
            self.update_case(case, 'Devolucion a emision de control de calidad')
            self.iniciar_facturacion(case)
        else:
            self.iniciar_facturacion(case)
    
    def iniciar_facturacion(self, case: Case):
        """
        Start billing.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Iniciar facturación')
        self.update_case(case, 'Generar Factura')
        # create a bill for every month from the last timestamp to today
        last_timestamp = case.last_timestamp
        while last_timestamp < timezone.now():
            Bill.objects.create(case=Case.objects.get(id=case.case_id), value=case.value, timestamp=last_timestamp)
            last_timestamp += timedelta(days=30)
        self.update_case(case, 'Contabilizar Factura')
        self.update_case(case, 'Generar poliza')
        self.update_case(case, 'Enviar factura electronica')
        self.update_case(case, 'Respuesta SRI')
        self.update_case(case, 'Enviar poliza electronica')
        self.update_case(case, 'Firma poliza electronica por parte del cliente')
        self.finalizar_poliza_factura_cliente(case)

    def finalizar_poliza_factura_cliente(self, case: Case):
        """
        Finish the policy invoice for the client.

        Args:
            case_id (str): The ID of the case.
            timestamp (datetime): The timestamp.
            case_type (str): The type of the case.
        """
        self.update_case(case, 'Finalizar envio poliza y factura al cliente')

        rand_num = random.randint(1, 100)

        if rand_num <= 80:
            self.update_case(case, 'Finalizar proceso de emision')
            self.update_case(case, 'Recepcion pago')

        
        elif rand_num <= 90:
            self.update_case(case, 'Devolucion a emision (corregir informacion)')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name='Finalizar envio poliza y factura al cliente').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.finalizar_poliza_factura_cliente(case)
        else:
            self.update_case(case, 'Devolucion a comercial (corregir informacion)')
            activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), timestamp=case.last_timestamp).first()
            return_activity = Activity.objects.filter(case=Case.objects.get(id=case.case_id), name='Finalizar envio poliza y factura al cliente').first()
            if return_activity:
                cost = (activity.timestamp - return_activity.timestamp).total_seconds()
            else:
                cost = 0
            Rework.objects.create(activity=activity, cost = cost)

            self.finalizar_poliza_factura_cliente(case)



    def create_variants(self, *args, **kwargs):
        """
        Create variants based on activities and their timestamps.
        """
        # List of cases to keep track of existing cases and identify case_index
        cases = []
        variants = defaultdict(list)
        timesPerCase = defaultdict(list)
        activities = Activity.objects.all()
    
        for activity in activities:
            case_id = activity.case.id
    
            if case_id not in cases:
                cases.append(case_id)
            case_index = cases.index(case_id)
            timestamp = activity.timestamp
    
            name = activity.name
    
            # Store the timestamp for calculating mean time
            timesPerCase[case_id].append(timestamp)
    
            # Get or create the case
            case, created = Case.objects.get_or_create(id=case_id)
    
            # Append activity name to the variants dictionary
            variants[case_id].append(name)
    
        # Grouping keys by their value lists
        grouped_data = defaultdict(list)
        for key, value in variants.items():
            grouped_data[tuple(value)].append(key)
    
        # Convert defaultdict to a regular dictionary and print the result
        grouped_data = dict(grouped_data)
    
        for key, value in grouped_data.items():
            number_cases = len(value)
            percentage = (number_cases / len(cases)) * 100
    
            # Calculate mean time for the variant
            total_duration = 0
            for case_id in value:
                times = timesPerCase[case_id]
                times.sort()
                duration = (times[-1] - times[0]).total_seconds()
                total_duration += duration
            mean_time = total_duration / number_cases
    
            Variant.objects.create(
                activities=str(key),
                cases=str(value),
                number_cases=number_cases,
                percentage=percentage,
                avg_time=mean_time
            )

    def add_TPT(self):
        index_list = Activity.objects.values_list('case_index', flat=True).distinct()
        for index in index_list:
            activities = Activity.objects.filter(case_index=index).order_by('timestamp')

            for i in range(len(activities) - 1):
                current_activity = activities[i]
                current_id = current_activity.id
                next_activity = activities[i + 1]

                time_diff = (next_activity.timestamp - current_activity.timestamp).total_seconds()
                Activity.objects.filter(id=current_id).update(tpt=time_diff)
   

    def get_case_activity_time(self):


        timesPerActivity = defaultdict(list)
        activities = Activity.objects.all()
        for activity in activities:
            timesPerActivity[activity.case.id].append({"ACTIVIDAD": activity.name, "TIMESTAMP": activity.timestamp})
        return timesPerActivity

    def get_mean_time_per_activity(self, timesPerActivity):
        activity_durations = defaultdict(list)
        for case_id, activities in timesPerActivity.items():
            for i in range(len(activities) - 1):
                current_activity = activities[i]
                next_activity = activities[i + 1]
                current_timestamp = current_activity["TIMESTAMP"]
                next_timestamp = next_activity["TIMESTAMP"]
                duration = abs(next_timestamp - current_timestamp)
                activity_durations[current_activity["ACTIVIDAD"]].append(duration.total_seconds())

        mean_time_per_activity = {}
        for activity, durations in activity_durations.items():
            mean_time_per_activity[activity] = sum(durations) / len(durations)

        mean_time_per_activity_json = json.dumps(mean_time_per_activity, indent=4)
        print(mean_time_per_activity_json)
        return mean_time_per_activity_json
    
    def add_time_to_cases(self):
        cases = Case.objects.all()
        for case in cases:
            activities = Activity.objects.filter(case=case).order_by('timestamp')
            last_activity = activities.last()
            first_activity = activities.first()
            case.avg_time = (last_activity.timestamp - first_activity.timestamp).total_seconds()
            case.save()
    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """

        for i in range(1000):
            self.start()
            if i % 100 == 0:
                self.stdout.write(self.style.SUCCESS(str(i) + 'instances added successfully'))
        self.stdout.write(self.style.SUCCESS('Adding time to cases'))
        self.add_time_to_cases()
        self.stdout.write(self.style.SUCCESS('Creating variants'))
        self.create_variants()
        self.stdout.write(self.style.SUCCESS('Adding TPT'))
        self.add_TPT()
        self.stdout.write(self.style.SUCCESS('Data added successfully'))

        self.get_mean_time_per_activity(self.get_case_activity_time())
