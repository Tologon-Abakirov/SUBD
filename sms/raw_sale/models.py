from django.db import models
from positions.models import Positions
from Rawmaterials.models import RawMaterials
from employees.models import Employees
from datetime import date
# Create your models here.
class RawMaterialPurchase(models.Model):
    RawMaterial_id = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, db_column='RawMaterial_id')
    Quantity = models.FloatField()
    Amount = models.DecimalField(max_digits=19, decimal_places=2)
    Date = models.DateField(default=date.today)  # Set default to today's date
    Employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='Employee_id')

    class Meta:
        db_table = 'RawMaterialPurchase'

    def __str__(self):
        return self.RawmMterial_id


