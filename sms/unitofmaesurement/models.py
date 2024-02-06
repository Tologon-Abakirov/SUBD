from django.db import models

class Unit(models.Model):
    Name = models.CharField(max_length=255)

    class Meta:
        db_table = 'UnitsOfMeasurement'

    def __str__(self):
        return self.Name