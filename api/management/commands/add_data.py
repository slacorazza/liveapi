import csv
from django.core.management.base import BaseCommand
from api.models import Invoice
from django.utils.dateparse import parse_datetime
from django.conf import settings
import os
import pandas as pd
from rapidfuzz import fuzz
import random


class Command(BaseCommand):
    """
    Django management command to add data to the database from a CSV file.
    """
    help = 'Add data to the database from CSV file'
    uniques = []


    def exact_match(row_a, row_b):
        """Coinciden exactamente los cuatro campos."""
        return (
            row_a['Invoice Reference'] == row_b['Invoice Reference'] and
            row_a['Document Date']    == row_b['Document Date']    and
            row_a['Invoice Value']    == row_b['Invoice Value']    and
            row_a['Vendor Name']      == row_b['Vendor Name']
        )

    def similar_vendor(row_a, row_b, threshold=90):
        """
        - 3 campos exactos: (Invoice Reference, Document Date, Invoice Value)
        - Vendor Name fuzzy con un mínimo de similitud (threshold).
        - Se ilustran algunas limpiezas mínimas (quitar caracteres no alfanuméricos).
        """
        if (
            row_a['Invoice Reference'] == row_b['Invoice Reference'] and
            row_a['Document Date']    == row_b['Document Date']    and
            row_a['Invoice Value']    == row_b['Invoice Value']
        ):
            def clean_vendor(name):
                # Quita todo lo que no sea alfanumérico
                cleaned = ''.join(ch for ch in name if ch.isalnum())
                return cleaned.upper()

            vend_a = clean_vendor(row_a['Vendor Name'])
            vend_b = clean_vendor(row_b['Vendor Name'])
            ratio = fuzz.token_sort_ratio(vend_a, vend_b)
            return ratio >= threshold
        return False

    def similar_reference(row_a, row_b, threshold=85):
        """
        - 3 campos exactos: (Document Date, Invoice Value, Vendor Name)
        - Invoice Reference fuzzy.
        - Se usa una métrica simple de similitud (rapidfuzz).
        """
        if (
            row_a['Document Date'] == row_b['Document Date'] and
            row_a['Invoice Value'] == row_b['Invoice Value'] and
            row_a['Vendor Name']   == row_b['Vendor Name']
        ):
            ref_a = ''.join(ch for ch in row_a['Invoice Reference'] if ch.isalnum())
            ref_b = ''.join(ch for ch in row_b['Invoice Reference'] if ch.isalnum())
            ratio = fuzz.token_sort_ratio(ref_a, ref_b)
            return ratio >= threshold
        return False

    def similar_date(row_a, row_b, max_days=7):
        """
        - 3 columnas exactas: (Invoice Reference, Invoice Value, Vendor Name)
        - Document Date difiere a lo sumo X días (por defecto, 7 días).
        - Se podría extender para día/mes invertido, etc.
        """
        if (
            row_a['Invoice Reference'] == row_b['Invoice Reference'] and
            row_a['Invoice Value']    == row_b['Invoice Value'] and
            row_a['Vendor Name']      == row_b['Vendor Name']
        ):
            try:
                d_a = pd.to_datetime(row_a['Document Date'])
                d_b = pd.to_datetime(row_b['Document Date'])
            except:
                return False
            
            diff = abs((d_a - d_b).days)
            return diff <= max_days
        return False

    def similar_value(row_a, row_b, tolerance=100):
        """
        - 3 columnas exactas: (Invoice Reference, Document Date, Vendor Name)
        - Invoice Value 'cerca' en el valor (<= tolerance).
        - O se pueden agregar más reglas (transposición de dígitos, etc.).
        """
        if (
            row_a['Invoice Reference'] == row_b['Invoice Reference'] and
            row_a['Document Date']    == row_b['Document Date'] and
            row_a['Vendor Name']      == row_b['Vendor Name']
        ):
            try:
                v_a = float(row_a['Invoice Value'])
                v_b = float(row_b['Invoice Value'])
                if abs(v_a - v_b) <= tolerance:
                    return True
            except:
                pass
        return False

    def get_match_patterns(self, row_a, row_b):
        """
        Devuelve una lista con TODOS los patrones que se cumplan
        (podría devolver más de uno a la vez si, p.ej., exact match y similar date
        se cumplen simultáneamente).
        """
        patterns = []
        if self.exact_match(row_a, row_b):
            patterns.append("exact match")
        if self.similar_vendor(row_a, row_b):
            patterns.append("similar vendor")
        if self.similar_reference(row_a, row_b):
            patterns.append("similar reference")
        if self.similar_date(row_a, row_b):
            patterns.append("similar date")
        if self.similar_value(row_a, row_b):
            patterns.append("similar value")
        return patterns


    def handle(self, *args, **kwargs):
        """
        Handle the command to add data to the database from the CSV file.
        """
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'api', 'data', 'Invoicesduplicates.csv')

        # Read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)


            for row in reader:
                invoice_ref = row['ï»¿Invoice']
                date = row['Document Date']
                value = row['Invoice Value']
                vendor = row['Vendor Name']
                pattern = ''
                open_ = random.choice([True, False])
                group_id = 0


                for unique in self.uniques:
                    patterns = self.get_match_patterns(row, unique)
                    if patterns.is_empty():
                        self.uniques.append(row)
                        pattern = 'unique'
                        group_id = 1
                    else:
                        pattern = ', '.join(patterns)
                        group_id = 2
                        if pattern.length > 19:
                            pattern = 'multiple'

                Invoice.objects.create(reference=invoice_ref, date=date, value=value, vendor=vendor, pattern=pattern, open=open_, group_id=group_id)
                    
        self.stdout.write(self.style.SUCCESS('Data added successfully'))