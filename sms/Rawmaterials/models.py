from django.db import models
from unitofmaesurement.models import Unit
class RawMaterials(models.Model):
    Name = models.CharField(max_length=255)
    Unit_of_measurement_id = models.ForeignKey(Unit, on_delete=models.CASCADE, db_column='Unit_of_measurement_id')

    Quantity = models.FloatField()
    Amount = models.FloatField()

    class Meta:
        db_table = 'RawMaterials'
    
    def __str__(self):
        return self.Name
