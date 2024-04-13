from django.db import models
from employees.models import Employees
from finishedproduct.models import Finishs
import datetime

date = datetime.datetime.now()

class ProductSale(models.Model):
    Product_id = models.ForeignKey(Finishs, on_delete=models.CASCADE, db_column='Product_id')
    Quantity = models.FloatField()
    Amount = models.FloatField()
    Date = models.DateField(default=date.today)
    Employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='Employee_id')

    class Meta:
        db_table = 'ProductSale'

