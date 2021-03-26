from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


# Create your models here.
class StoreUser(AbstractUser):
    UserWallet = models.PositiveIntegerField(default=10000)

    def __str__(self):
        return "{}".format(self.username)


class Snus(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='media', default='default.jpg', blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}".format(self.title)


class Purchase(models.Model):
    customer = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Snus, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_time = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return "{} from {} ".format(self.product, self.customer)


class ReturnPurchase(models.Model):
     purchase_return = models.ForeignKey(Purchase, on_delete=models.CASCADE)
     time_of_return =models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return "{} wanted to return at {}".format(self.purchase_return, self.time_of_return)

