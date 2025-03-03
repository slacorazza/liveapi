import csv
from django.core.management.base import BaseCommand
from api.models import Case, Activity, Variant
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
from collections import defaultdict
from datetime import datetime

class Command(BaseCommand):
    """
    Django management command to add data to the database from a CSV file.
    """
    help = 'Add data to the database from CSV file'

    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
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
                minutes, seconds_fraction = timestamp_str.split(':')
                seconds, fraction = seconds_fraction.split('.')
                timestamp_str_corrected = f"{minutes}:{seconds}.{fraction}00000"
                timestamp = datetime.strptime(timestamp_str_corrected, '%M:%S.%f')

                
                name = row['ACTIVIDAD']

                # Store the timestamp for calculating mean time
                timesPerCase[case_id].append(timestamp)

                #print(case_id, timestamp_str, timestamp_formatted, name, case_index)
                # Get or create the case
                case, created = Case.objects.get_or_create(id=case_id)

                # Create the activity
                Activity.objects.create(case=case, timestamp=timestamp, name=name, case_index=case_index)
            
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
                    mean_time=mean_time
                )

        self.stdout.write(self.style.SUCCESS('Data added successfully'))