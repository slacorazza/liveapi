import os
import csv

def handle(self, *args, **kwargs):
    """
    Handle the command to add data to the database from the CSV file.
    """
    # Path to the CSV file
    csv_file_path = os.path.join('.', 'api', 'data', 'Invoicesduplicates.csv')

    # Read the CSV file
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
