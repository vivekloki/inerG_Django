# serializers.py
from rest_framework import serializers
from .models import Organization

class AnnualDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['api_well_number', 'oil', 'gas', 'brine']
        # fields='__all__' 
