from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=20)
    amount = models.CharField(max_length=100)
    payment_id=models.CharField(max_length=200,blank=True)
    order_id=models.CharField(max_length=20,blank=True)
    is_paid=models.BooleanField(default=False)
    
    def __str__(self):
        
        return str(self.name)