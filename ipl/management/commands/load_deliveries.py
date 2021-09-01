from django.core.management.base import BaseCommand
import csv
import os
from django.conf import settings
from ipl.models import Deliveries
import gc
from django import db
from django.db import transaction



from collections import defaultdict
from django.apps import apps


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'

    def handle(self, *args, **options):
        data_folder = os.path.join(str(settings.BASE_DIR), 'data')
        csv_name = 'deliveries.csv'
        file_path = os.path.join(data_folder, 'deliveries.csv')
        Deliveries.objects.all().delete()
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            dict_list = []
            id_list = []
            for i, line in enumerate(reader):
                line_list = list(line.items())                        
                dict_list.append({x[0]: x[1] for x in line_list})

            start_id = 0
            total_count = len(dict_list)
            print("Total count of Deliveries is %s" % (total_count))
            while start_id < total_count:
                end_id = start_id + 50
                print("Loading %s to %s" %(start_id, end_id))
                to_be_inserted = dict_list[start_id:end_id]
                for _object_dict in to_be_inserted:
                    Deliveries.objects.create(**_object_dict)
                start_id = end_id              
                db.reset_queries()
                gc.collect()
        print(Deliveries.objects.all().count())