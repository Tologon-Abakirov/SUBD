from django.db import models
from employees.models import Employees
from finishedproduct.models import Finishs

# Create your models here.
class Production(models.Model):
    Product_id = models.ForeignKey(Finishs, on_delete=models.CASCADE, db_column='Product_id')
    Quantity = models.FloatField()
    Date = models.DateField()
    Employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='Employee_id')

    class Meta:
        db_table = 'Production'
    
    def __str__(self):
        return self.Product_id