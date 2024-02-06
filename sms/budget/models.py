from django.db import models

# Create your models here.
class Budget(models.Model):
    Budget_Amount= models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'Budget'
