from django.db import models
from positions.models import Positions

# Create your models here.
class Employees(models.Model):
    Full_Name = models.CharField(max_length=255, db_column='Full_Name')
    Position = models.ForeignKey(Positions, on_delete=models.CASCADE, db_column='Position')
    Salary = models.CharField(max_length=19,  db_column='Salary')
    Address = models.CharField(max_length=255, db_column='Address')
    Phone = models.CharField(max_length=15, db_column='Phone')

    class Meta:
        db_table = 'Employees'
    
    def __str__(self):
        return self.Full_Name

