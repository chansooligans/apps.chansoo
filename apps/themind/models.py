from django.db import models

class RandomNumber(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    user_name = models.CharField(max_length=50)
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.value1}, {self.value2} in {self.room_name} by {self.user_name}"