

from typing import Iterator
from django.shortcuts import redirect, render
from pkg_resources import cleanup_resources
import datetime


from .models import *
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
import random
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from payment.models import *
from django.core.mail import send_mail
from celery.schedules import crontab
from celery.task import periodic_task



# Create your views here.
def index(request):
    return render(request,'index.html')
    
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phonenumber=request.POST.get('phonenumber')
        message=request.POST.get('message')
    
        Contact.objects.create(
            name=name,
            email=email,
            phonenumber=phonenumber,
            message=message
        )

        return render(request,'index.html',{'msg':'Successfull'})
    return render(request,'index.html')

def register(request):
    registered=False
    
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.save()
            print(user.email)
            a=user.email
            profile=profile_form.save(commit=False)
            profile.user=user
            upi=randomGen()
            print(upi)
            profile.upi=upi
            profile.save()
            send_mail('Secret Key','Plaese Note the secret key '+str(upi),'shabi960580@gmail.com',[a])
            

            registered=True
        else:
            HttpResponse('Invalid form')
    else:
        user_form=UserForm()
        profile_form=ProfileForm()
    return render(request,'index.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})


def user_login(request):

    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                if user.is_superuser:
                    login(request,user)
                    return HttpResponseRedirect(reverse('account_dashboard'))
                else:
                    login(request,user)
                    return HttpResponseRedirect(reverse('login2'))

            else:
                 return HttpResponse('user not active')
        else:
            return HttpResponse('invalid username or password ')
    else:
        return render(request,'login.html')



def login2(request):
    if request.method=="POST":
        upi=request.POST.get('upi')
        try:
            user=Register.objects.get(upi=upi)
        except:
            return HttpResponse("Invalid upi")
        if user:
            
                
            return HttpResponseRedirect(reverse('account_dashboard'))
        else:
            return HttpResponse('Not a user')
        
    else:
        return render(request,'login2.html')



def user_logout(request):
    logout(request)
    return redirect('index')



def customer_dashboardtable(request):
    return render(request,'tables.html')


def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))

def account_dashboard(request):
    
    try:
        curr_user = BankAccount.objects.filter(user=request.user) # getting details of current user
    except:
        return redirect("create_account")
    
         
    return render(request, "account_dashboard.html", {"curr_user": curr_user})
    












# def emicomplete(request):
    
#     if request.method=='POST':
#         a=float(request.POST.get('total_amount'))
#         b=float(request.POST.get('paid'))
#         c=a-b
#         print(c)

#         EMIPayment.objects.update_or_create(
#             Total_amount_paid=a,
#             paid_amount=b   
#         )
#         return redirect('emicomplete')
#     return render(request,'emicomplete.html')








def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"YOUR PASSWORD SUCCEFULLY UPDATED")
            return redirect('account_dashboard')
        else:
            messages.error(request,'PLEASE CORRECT ERROR')
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'change_password.html',{'form':form})






def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.register)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account_dashboard')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.register)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)

def chat(request):
    if request.method=='POST':
        a=request.POST.get('doubt')

        Complaint.objects.create(
            user=request.user,
            content=a
        )
        messages.success(request,'we will contact you otherwise check your chat status')

        return redirect('account_dashboard')  
    return render(request,'chat.html')

def chatupdate(request,todo_id):
    todo=Complaint.objects.get(id=todo_id)
    form=ComplaintForm(instance=todo)
    if request.method=='POST':
        form=ComplaintForm(request.POST,instance=todo)
        form.save()
        return redirect('account_dashboard')
    return render(request,'chatupdate.html',{'form':form})

def allchat(request):
    all=Complaint.objects.all()
    return render(request,'view_chat.html',{'all':all})

def chatuserview(request):
    all=Complaint.objects.filter(user=request.user).order_by('-date')
    return render(request,'chatstatus.html',{'all':all})




def create_account(request):
    
    bank=Bank.objects.all()
    if request.method=="POST":
        bank=request.POST.get('bank')
        bank1=Bank.objects.get(bankname=bank)
        print(bank1.bankname)
        aadhar=request.POST.get('aadhar')
        balance=request.POST.get('balance')
        print(bank)
        print(aadhar)

        account=BankAccount.objects.create(
            bank=bank1,
            aadhar=aadhar,
            user=request.user,
            balance=balance,
            account_no = randomGen()
        )
        
            
        account.save()

                
        return render(request,'create_account.html',{'msg':'successfully added complaint'})

    return render(request,'create_account.html',{'bank':bank})



def view_my_accounts(request):
    try:
        curr_user = BankAccount.objects.filter(user=request.user) # getting details of current user
    except:
        return redirect("create_account")
    
         
    return render(request, "view_my_accounts.html", {"curr_user": curr_user})



def view_reciever_accounts(request,account_id):
    #account_id1=request.user.account_id
    print(account_id)
    request.session['account_id']=account_id

    if request.method=="POST":
        aadhar=request.POST.get('aadhar')
        try:
            account=BankAccount.objects.filter(aadhar=aadhar)
            print(account)
            return render(request,'receiver_account.html',{'account':account})
        except:
            pass
    return render(request,'receiver_account.html')



def amount_transfer(request,receiver_account_id):
    sender_account_id=request.session['account_id']
    sender_account_no=BankAccount.objects.get(id=sender_account_id)
    receiver_account_no=BankAccount.objects.get(id=receiver_account_id)
    print(sender_account_no)
    print(receiver_account_no)
    sender_name=BankAccount.objects.filter(user=request.user)
    
    
    print(sender_name)
    if request.method=="POST":
        sender_account_id=request.session['account_id']
        sender_account_no=BankAccount.objects.get(id=sender_account_id)
        receiver_account_no=BankAccount.objects.get(id=receiver_account_id)
        print(sender_account_no)
        print(receiver_account_no)
        sender_name=BankAccount.objects.filter(user=request.user)
        enter_your_user_name=request.user.username
        enter_the_destination_account_number=receiver_account_no.account_no
        amount=request.POST.get('amount')
        upi=request.POST.get('upi')
        try:
            valid_user=Register.objects.get(upi=upi,user=request.user)
        except:
            return HttpResponse("Invalid upi")
        if valid_user:
            receiver=BankAccount.objects.filter(account_no=enter_the_destination_account_number)
            receiver_name=BankAccount.objects.get(account_no=enter_the_destination_account_number)
            print(receiver_name.user)
            name=enter_your_user_name==request.user.username
            if receiver.exists() and name:
                payment=MoneyTransfer.objects.create(
                    enter_your_user_name=enter_your_user_name,
                    enter_the_destination_account_number=enter_the_destination_account_number,
                    enter_the_amount_to_be_transferred_in_INR=amount,
                    sender_account_no=sender_account_no.account_no,
                    receiver_name=receiver_name.user.username

                )
                payment.save()
                amount=int(amount)
                curr_user=BankAccount.objects.get(id=sender_account_id)
                dest_user=BankAccount.objects.get(id=receiver_account_id)
                print(curr_user)
                print(dest_user)
                curr_user.balance = curr_user.balance - amount
                dest_user.balance = dest_user.balance + amount
                print(curr_user.balance)
                if curr_user.balance < 500 :
                    messages.error(request,'current balance is minimum 500 not possible tranfer money')
                else:   
                    curr_user.save()
                    dest_user.save()
            
                return redirect('account_dashboard')
            else:
                return HttpResponse("Sender or receiver does not exist")
        else:
            return HttpResponse("Invalid upi")

    return render(request,'amount_transfer.html')





def history(request):
    user1=MoneyTransfer.objects.filter(enter_your_user_name=request.user.username).order_by('-date')
    print(user1)
    user2=MoneyTransfer.objects.filter(receiver_name=request.user.username).order_by('-date')
    print(user2)
    return render(request,'history.html',{'user1':user1,'user2':user2})


def paymentview(request):
    payment=Payment.objects.filter(user=request.user)
    return render(request,'paymentview.html',{'payment':payment})     
       


def add_reminder(request):
    if request.method=="POST":
        reminder_form=ReminderForm(request.POST)
        if reminder_form.is_valid():
            cp=Reminder(user=request.user,title=reminder_form.cleaned_data['title'],content=reminder_form.cleaned_data['content'],reminder_date=reminder_form.cleaned_data['reminder_date'])
            cp.save()
            user=cp.user
            register=Register.objects.get(user=user)
            print(register.user.email)
            a=register.user.email
            title=cp.title
            content=cp.content
            date=cp.reminder_date
            send_mail('title: '+title,'content: '+content+  ',   date: '+str(date),'shabi960580@gmail.com', [a])

            
            return HttpResponseRedirect('view_reminder')
        else:
            return HttpResponse("Invalid form")
    reminder_form=ReminderForm()
    return render(request,'reminder.html',{'form':reminder_form})


def view_reminder(request):
    reminder=Reminder.objects.filter(user=request.user)
    return render(request,'reminder_view.html',{'reminder':reminder})



def reports(request):
    return render(request,'reports.html')


def transaction_report(request):
    user1=MoneyTransfer.objects.filter(enter_your_user_name=request.user.username).order_by('-date')
    print(user1)
    user2=MoneyTransfer.objects.filter(receiver_name=request.user.username).order_by('-date')
    print(user2)
    user3=MoneyTransfer.objects.all().order_by('-id')
    return render(request,'transaction_report.html',{'user1':user1,'user2':user2,'user3':user3})


def reminder_report(request):
    reminder=Reminder.objects.filter(user=request.user).order_by('-id')
    all_reminder=Reminder.objects.all().order_by('-id')
    return render(request,'reminder_report.html',{'reminder':reminder,'all_reminder':all_reminder})


def complaint_report(request):
    complaints=Complaint.objects.filter(user=request.user).order_by('-id')
    all_complaints=Complaint.objects.all().order_by('-id')
    return render(request,'complaint_report.html',{'complaints':complaints,'all_complaints':all_complaints})


def payment_report(request):
    payments=Payment.objects.filter(user=request.user).order_by('-id')
    all_payments=Payment.objects.all().order_by('-id')
    return render(request,'payment_report.html',{'payments':payments,'all_payments':all_payments})

def registration_report(request):
    all_registrations=Register.objects.all().order_by('-id')
    return render(request,'registration_report.html',{'all_registrations':all_registrations})


def locations(request):
    return render(request,'locations.html')





        

    