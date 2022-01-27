from django.db.models import fields
from django.db.models.expressions import F
from django.forms import widgets
from django.forms.widgets import PasswordInput, Widget
from .models import *
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(UserCreationForm):
    username=forms.CharField(help_text=None,max_length=20,label='UserName')
    password1=forms.CharField(help_text=None,label='Password',widget=PasswordInput)
    password2=forms.CharField(help_text=None,label='Password Confirm',widget=PasswordInput)

    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
        labels=('password1','Password',
        'password2','Confirm_Password')

class ProfileForm(forms.ModelForm):
    address=forms.Textarea()
    class Meta:
        model=Register
        fields=('image',)

class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model =MoneyTransfer
        fields = [
            "enter_your_user_name",
            "enter_the_destination_account_number", 
            "enter_the_amount_to_be_transferred_in_INR"
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['image']



class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields="__all__"



class BankAccountForm(forms.ModelForm):
    class Meta:
        model=BankAccount
        fields=('bank','aadhar')


class ReminderForm(forms.ModelForm):
    content=forms.Textarea()
    reminder_date=forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=Reminder
        fields=('title','content','reminder_date')