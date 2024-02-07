from django.db import models

# Create your models here.
class Budget(models.Model):
    Budget_Amount = models.CharField(max_length=255)

    class Meta:
        db_table = 'Budget'
