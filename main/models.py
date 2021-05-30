from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User  , on_delete=models.CASCADE , null=True )
    wallet_amount = models.FloatField()
  
class Favourites(models.Model):
    account = models.ForeignKey(Account , on_delete=models.CASCADE , null=True)
    name = models.TextField()
    price= models.CharField(max_length = 20)
    img = models.URLField()
    link = models.URLField()
    website = models.CharField(max_length=10 , null=True)
    def __str__(self):
        return str(self.name) + '-' + str(self.price) + '-' + str(self.website)


class Requests(models.Model):
    account = models.ForeignKey(Account , on_delete=models.CASCADE , null=True)
    requestedmoney= models.FloatField()
    requester_username = models.CharField(max_length=20)
    requester_id = models.IntegerField(null=True)

    
class Notifications(models.Model):
    account = models.ForeignKey(Account , on_delete=models.CASCADE , null=True)
    content = models.TextField()
    def __str__(self):
        return str(self.content)



