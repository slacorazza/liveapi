from django.db import models
from .constants import PATTERN_CHOICES

class Invoice(models.Model):
    """
    Model representing an invoice.

    Attributes:
        reference (str): The unique reference for the invoice.
        date (datetime): The date of the invoice.
        value (decimal): The value of the invoice.
        vendor (str): The name of the vendor without code.
        pattern (str): The pattern type of the invoice.
        open (bool): Thestatus of the invoice, can be open or closed.
        group_id (str): The group ID associated with the invoice.
        confidence (str): The confidence level of the invoice.
    """
    reference = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=50)
    pattern = models.CharField(max_length=50, choices=PATTERN_CHOICES)
    open = models.BooleanField(default=True)
    group_id = models.CharField(max_length=50)
    confidence = models.CharField(max_length=6)

    def __str__(self):
        return f"Invoice {self.reference} from {self.vendor} on {self.date}"