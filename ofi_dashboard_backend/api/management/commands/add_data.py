import csv
from django.core.management.base import BaseCommand
from api.models import Case, Activity
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Add data to the database from CSV file'

    cases = []

    def if_case_exists(self, case_id):
        for case in self.cases:
            if case.id == case_id:
                return True
        return False

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'tabla_actividades.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            cases = []
            for row in reader:
                case_id = row['ID']
                if case_id not in cases:
                    cases.append(case_id)
                case_index = cases.index(case_id)
                timestamp = parse_datetime(row['TIMESTAMP'])
                name = row['ACTIVIDAD']

                print(case_id, timestamp, name, case_index)
                # Get or create the case
                case, created = Case.objects.get_or_create(id=case_id)

                # Create the activity
                Activity.objects.create(case=case, timestamp=timestamp, name=name, case_index=case_index)

        self.stdout.write(self.style.SUCCESS('Data added successfully'))