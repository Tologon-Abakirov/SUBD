from django.db import models

# Create your models here.
class Budget(models.Model):
    Budget_Amount= models.FloatField()
    Percent=models.FloatField()
    Bonus=models.FloatField()
    class Meta:
        db_table = 'Budget'
