from django.db import models
from accounts.models import FarmUser,CustUser
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.forms import ValidationError

# Create your models here.
app_name='farmuser'
User=get_user_model()

class Farm(models.Model):
    user=models.ForeignKey(User,related_name="farm_owner",on_delete=models.CASCADE)
    farmname=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True,null=True)
    SizeOfFarm=models.IntegerField()
    image=models.ImageField(upload_to="farms",blank=True, null=True, default='‪seee.jpg')
    address=models.TextField(default='')
    area=models.CharField(default='',max_length=20)
    city=models.CharField(default='',max_length=20)
    pincode=models.IntegerField()

    def __str__(self):
        return self.farmname

    def save(self,*args,**kwargs):
        self.slug = slugify(self.farmname)
        super().save(*args,**kwargs)
    
    class Meta:
        ordering = ('-id',)

 
class FarmImage(models.Model):
    farm = models.ForeignKey(Farm, related_name="farm_image", on_delete=models.CASCADE)
    image = models.FileField(upload_to='farms/',blank=True, null=True, default='‪seee.jpg')


 

def validate_date(date):
    if date.strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
        raise ValidationError("Date cannot be in the past")

class FarmAvailble(models.Model):
    farm=models.ForeignKey(Farm,related_name="available_dates",on_delete=models.CASCADE)
    farmprice=models.IntegerField()
    available=models.DateField(validators=[validate_date])
    is_booked=models.BooleanField(default=False)
    booking_order_id=models.CharField(max_length=100,default='',null=True)

    class Meta:
       unique_together = ("farm", "available")
      

class FarmBooking(models.Model):
    user=models.ForeignKey(User,related_name="user_booking",on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, related_name="farm_booking", on_delete=models.CASCADE)
    farmavailable = models.ForeignKey(FarmAvailble, related_name="farm_available", on_delete=models.CASCADE,default="",null=True)
    booking_date=models.DateTimeField(auto_now=True)
    farm_booking_date=models.DateField(validators=[validate_date])
    price=models.IntegerField()
    booking_order_id=models.CharField(max_length=100,default='',null=True)
    No_of_People=models.IntegerField( default=1)


