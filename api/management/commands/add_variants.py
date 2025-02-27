import csv
from django.core.management.base import BaseCommand
from api.models import Case, Activity, Variant
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
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
            for row in reader:
                
                case_id = row['ID']
                #If the case is not in the list of cases, add it
                if case_id not in cases:
                    cases.append(case_id)
                case_index = cases.index(case_id)

                timestamp = parse_datetime(row['TIMESTAMP'])
                name = row['ACTIVIDAD']

                #print(case_id, timestamp, name, case_index)
                # Get or create the case
                case, created = Case.objects.get_or_create(id=case_id)

                # Create the activity
                Activity.objects.create(case=case, timestamp=timestamp, name=name, case_index=case_index)
            
            reader = csv.DictReader(csvfile)

            for case in cases:
                #print('CASEEEEEEEEE',case)
                variants[case] = []
                csvfile.seek(0)
                for row in reader:
                    #print(row['ID'], case)
                    if row['ID'] == case:
                        #print (row['ID'], case)
                        variants[case].append(row['ACTIVIDAD'])
                #print(case, variants[case])

            # Grouping keys by their value lists
            grouped_data = defaultdict(list)
            for key, value in variants.items():
                grouped_data[tuple(value)].append(key)

            # Convert defaultdict to a regular dictionary and print the result
            grouped_data = dict(grouped_data)
            #for key, value in grouped_data.items():
            
            for key, value in grouped_data.items():
                #print(key, value)
                number_cases = len(value)
                percentage = (number_cases/len(cases))*100
                Variant.objects.create(activities=str(key), cases=str(value), number_cases=number_cases, percentage=percentage) 

           

            

        self.stdout.write(self.style.SUCCESS('Data added successfully'))