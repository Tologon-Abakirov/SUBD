from django.db import models
from employees.models import Employees

class Salary(models.Model):
    Year = models.IntegerField()
    Month = models.IntegerField()
    Employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    Number_of_purchases = models.IntegerField()
    Number_of_productions = models.IntegerField()
    Number_of_sales = models.IntegerField()
    Common = models.IntegerField()
    Salary = models.FloatField()
    Bonus = models.FloatField()
    General = models.FloatField()
    Given = models.BooleanField()

    class Meta:
        db_table = 'Salary'
