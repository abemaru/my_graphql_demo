from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    brand = models.CharField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name


class User(models.Model):
    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.name