
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phonenumber=PhoneNumberField()
    message=models.TextField()

    def __str__(self):
        return str(self.name)

class Register(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile',default='user.jpg')
    account_number=models.IntegerField(blank=True,null=True)
    customer='customer'
    manager='manager'
    user_types=[(customer,'customer'),(manager,'manager')]
    user_type=models.CharField( max_length=50,choices=user_types,default=customer)
    upi=models.IntegerField()
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user.username) 




class MoneyTransfer(models.Model):
    enter_your_user_name = models.CharField(max_length = 150,blank=True,null=True)
    enter_the_destination_account_number = models.IntegerField()
    enter_the_amount_to_be_transferred_in_INR = models.IntegerField()
    sender_account_no=models.IntegerField(null=True,blank=True)
    receiver_name=models.CharField(max_length=30,null=True,blank=True)
    date=models.DateTimeField(default=timezone.now)
               


    



class Complaint(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    content=models.TextField()
    ans=models.TextField(blank=True,null=True)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)



class Bank(models.Model):
    bankname=models.CharField(max_length=30)
    bankcode=models.CharField(max_length=30)
    def __str__(self):
        return str(self.bankname)


class BankAccount(models.Model):
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,blank=True,null=True)
    account_no=models.IntegerField(blank=True,null=True)
    aadhar=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    balance = models.IntegerField(null=True,blank=True,default=0)
    def __str__(self):
        return str(self.account_no)

    

class Reminder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50)
    content=models.TextField()
    reminder_date=models.DateField()
    date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.user.username)


