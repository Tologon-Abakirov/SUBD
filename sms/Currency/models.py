from django.db import models

# Create your models here.
class Currency(models.Model):
    Name = models.CharField(max_length=255)


    class Meta:
        db_table = 'Currency'

    def __str__(self):
        return self.Name