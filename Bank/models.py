from django.db import models
from django.utils import timezone

# user craetion models
class Userform(models.Model):
    name        = models.CharField(max_length=50)
    email       = models.EmailField(max_length=254)
    balance     = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# transaction models
class Transferform(models.Model):
    sender_name          = models.CharField(max_length=50)
    receiver_name        = models.CharField(max_length=50)
    amount               = models.IntegerField(default=0)
    date                 = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.sender_name
