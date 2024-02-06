from django.db import models
from employees.models import Employees
from finishedproduct.models import Finishs
from Currency.models import Currency

class ProductSale(models.Model):
    Product_id = models.ForeignKey(Finishs, on_delete=models.CASCADE, db_column='Product_id')
    Quantity = models.FloatField()
    Amount = models.DecimalField(max_digits=19, decimal_places=0)
    Currency = models.ForeignKey(Currency, on_delete=models.CASCADE, db_column='Name')
    Date = models.DateField()
    Employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='Employee_id')

    class Meta:
        db_table = 'ProductSale'

