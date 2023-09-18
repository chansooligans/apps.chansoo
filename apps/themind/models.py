from django.db import models

class RandomNumber(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()

    def __str__(self):
        return f"{self.value1}, {self.value2}"