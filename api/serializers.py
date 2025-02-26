from rest_framework import serializers
from .models import Invoice

## Serializers are used to convert complex data types, such as querysets and model instances, to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.

    Converts Invoice model instances to native Python datatypes that can be easily rendered into JSON, XML, or other content types.

    Meta:
        model (Invoice): The model that is being serialized.
        fields (tuple): The fields of the model that should be included in the serialized output.
    """

    value = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    
    class Meta:
        model = Invoice
        fields = 'reference', 'date', 'value', 'vendor', 'pattern', 'open', 'group_id', 'confidence'