from django.db import models
from django.contrib import auth
from twilio.rest import Client
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.

User=get_user_model()

class FarmUser(auth.models.User,auth.models.PermissionsMixin):
    # user=models.OneToOneField(User,related_name="farm_user",on_delete=models.CASCADE,null=True)
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    mobile=models.IntegerField(unique=True,null=True)
    otp=models.IntegerField(default=0)

    def __str__(self):
        return "@{}".format(self.username)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.username)
        # self.user=self.request.user
        super().save(*args,**kwargs)


class CustUser(auth.models.User,auth.models.PermissionsMixin):
    # user=models.OneToOneField(User,related_name="cust_user",on_delete=models.CASCADE)
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    mobile=models.IntegerField(unique=True,null=True)

    def __str__(self):
        return "@{}".format(self.username)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.username)
        # self.user=self.request.user
        super().save(*args,**kwargs)