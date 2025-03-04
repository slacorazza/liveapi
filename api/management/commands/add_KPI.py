import csv, json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
from collections import defaultdict
from datetime import datetime

class Command(BaseCommand):

    def get_case_activity_time(self):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'tabla_actividades.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            timesPerActivity = defaultdict(list)
            for row in reader:
                timesPerActivity[row["ID"]].append({"ACTIVIDAD": row["ACTIVIDAD"], "TIMESTAMP": row["TIMESTAMP"]})
            return timesPerActivity

    def get_mean_time_per_activity(self, timesPerActivity):
        activity_durations = defaultdict(list)
        for case_id, activities in timesPerActivity.items():
            for i in range(len(activities) - 1):
                current_activity = activities[i]
                next_activity = activities[i + 1]
                current_timestamp = datetime.strptime(current_activity["TIMESTAMP"], "%Y-%m-%d %H:%M:%S")
                next_timestamp = datetime.strptime(next_activity["TIMESTAMP"], "%Y-%m-%d %H:%M:%S")
                duration = abs(next_timestamp - current_timestamp)
                activity_durations[current_activity["ACTIVIDAD"]].append(duration.total_seconds())

        mean_time_per_activity = {}
        for activity, durations in activity_durations.items():
            mean_time_per_activity[activity] = sum(durations) / len(durations)

        mean_time_per_activity_json = json.dumps(mean_time_per_activity, indent=4)
        print(mean_time_per_activity_json)
        return mean_time_per_activity_json
        
    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
        self.get_mean_time_per_activity(self.get_case_activity_time())