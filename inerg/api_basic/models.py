from django.db import models

class Organization(models.Model):
    """Table for defining the organization details"""
    api_well_number = models.IntegerField(null=True, unique=True)
    oil = models.IntegerField(null=True)
    gas = models.IntegerField(null=True)
    brine = models.IntegerField(null=True)

    def __str__(self):
        return str(self.api_well_number)