import csv
from django.core.management.base import BaseCommand
from api.models import Case, Activity, Variant
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
from datetime import datetime
from collections import defaultdict

class Command(BaseCommand):
    """
    Django management command to add data to the database from a CSV file.
    """
    help = 'Add data to the database from CSV file'

    def if_case_exists(self, case_id):
        """
        Check if a case with the given ID already exists in the list of cases.

        Args:
            case_id (str): The ID of the case to check.

        Returns:
            bool: True if the case exists, False otherwise.
        """
        for case in self.cases:
            if case.id == case_id:
                return True
        return False

    def create_cases(self):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'tabla_actividades.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            timesPerCase = defaultdict(list)
            for row in reader:
                case_id = row['ID']
                timestamp = datetime.strptime(row['TIMESTAMP'], "%Y-%m-%d %H:%M:%S")
                timesPerCase[case_id].append(timestamp)
            CasesMeanTime = {}
            for case_id in timesPerCase.keys():
                times = timesPerCase[case_id]
                times.sort()
                meanTime = times[-1] - times[0]
                CasesMeanTime[case_id] = meanTime.total_seconds()
                # Add the mean time to the case
                case, created = Case.objects.get_or_create(id=case_id, defaults={'avg_time': meanTime.total_seconds()})

    def create_variants(self, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'tabla_actividades.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            # List of cases to keep track of existing cases and identify case_index
            cases = []
            variants = {}
            timesPerCase = defaultdict(list)
            for row in reader:
                case_id = row['ID']
                # If the case is not in the list of cases, add it
                if case_id not in cases:
                    cases.append(case_id)
                case_index = cases.index(case_id)

                timestamp_str = row['TIMESTAMP']
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                name = row['ACTIVIDAD']

                # Store the timestamp for calculating mean time
                timesPerCase[case_id].append(timestamp)

                # Get or create the case
                case, created = Case.objects.get_or_create(id=case_id)
            
            reader = csv.DictReader(csvfile)

            for case in cases:
                variants[case] = []
                csvfile.seek(0)
                for row in reader:
                    if row['ID'] == case:
                        variants[case].append(row['ACTIVIDAD'])

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

    def create_activities(self):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'tabla_actividades.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            # List of cases to keep track of existing cases and identify case_index
            cases = []
            for row in reader:
                case_id = row['ID']
                # If the case is not in the list of cases, add it
                if case_id not in cases:
                    cases.append(case_id)
                case_index = cases.index(case_id)

                timestamp_str = row['TIMESTAMP']
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                name = row['ACTIVIDAD']

                # Get or create the case
                case, created = Case.objects.get_or_create(id=case_id)

                # Create the activity
                Activity.objects.create(case=case, timestamp=timestamp, name=name, case_index=case_index)

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



    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
        self.create_cases()
        self.create_activities()
        self.create_variants()
        self.add_TPT()

        self.stdout.write(self.style.SUCCESS('Data added successfully'))