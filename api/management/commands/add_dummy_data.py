import csv
from django.core.management.base import BaseCommand
from api.models import Invoice
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
import pandas as pd
from rapidfuzz import fuzz
import random
from datetime import datetime, timedelta

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
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'DummyData.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)


            for row_number, row in enumerate(reader, start=1):
                invoice_ref = 'INV-' + str(row_number)
                date_str = row['Earliest Due Date']
                if date_str == '':
                    date = datetime(2024, 1, 1) + timedelta(days=row_number)
                else:
                    date = parse_datetime(date_str)
                    # Convert date from MM/DD/YYYY to YYYY-MM-DD format
                    try:
                        date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        raise ValueError(f"Invalid date format: {date_str} in row {row_number}")
                value = row['Group Value']
                vendor = row['Vendor']
                pattern = row['Group Pattern']
                open_ = random.choice([True, False])
                group_id = row['Group UUID']

                if 'Open' in row['Group Contains']:
                    open_ = True
                else:
                    open_ = False

                Invoice.objects.create(reference=invoice_ref, date=date, value=value, vendor=vendor, pattern=pattern, open=open_, group_id=group_id)
                    
        self.stdout.write(self.style.SUCCESS('Data added successfully'))