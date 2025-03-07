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

    def get_caseindex_list(self):
        activities = Activity.objects.all()
        case_index_list = []

        for activity in activities:
            if activity.case_index not in case_index_list:
                case_index_list.append(activity.case_index)
        return case_index_list
    
    def get_pair_activities(self, case_index):
        # Get all activities pair for a case index and the time difference between them
        activities = Activity.objects.filter(case_index=case_index).order_by('timestamp')
        activity_pairs = defaultdict(lambda: {'time_difference': 0, })
        for i in range(len(activities) - 1):
            current_activity = activities[i]
            next_activity = activities[i + 1]
            pair = (current_activity.name, next_activity.name)
            time_diff = (next_activity.timestamp - current_activity.timestamp).total_seconds()
            activity_pairs[pair]['time_difference'] += time_diff
        return activity_pairs


    def get_pair_list(self, case_index):
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
        
       

    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
        print(self.get_pair_activities(1))