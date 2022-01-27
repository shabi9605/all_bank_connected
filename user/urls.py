from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name="index"),
    path('contact',views.contact,name='contact'),
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('login2',views.login2,name='login2'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('account_dashboard/',views.account_dashboard,name='account_dashboard'),
    path('customer_dashboardtable/',views.customer_dashboardtable,name='customer_dashboardtable'),
    
    # path('emicomplete',views.emicomplete,name='emicomplete'),
    path('password',views.change_password,name="password"),
    path('profile/',views.profile, name='profile'),
    path('chat',views.chat,name='chat'),
    path('allchat',views.allchat,name='allchat'),
    path('chatupdate/<int:todo_id>',views.chatupdate,name="chatupdate"),
    path('mychat',views.chatuserview,name='mychat'),
    
    path('paymentview',views.paymentview,name='paymentview'),
    
    path('create_account',views.create_account,name="create_account"),
    path('amount_transfer/<int:receiver_account_id>',views.amount_transfer,name="amount_transfer"),
    
    path('history',views.history,name="history"),
    path('add_reminder',views.add_reminder,name="add_reminder"),
    path('view_reminder',views.view_reminder,name="view_reminder"),
    path('view_my_accounts',views.view_my_accounts,name='view_my_accounts'),
    path('view_reciever_accounts/<int:account_id>',views.view_reciever_accounts,name='view_reciever_accounts'),


    path('reports',views.reports,name='reports'),
    path('transaction_report',views.transaction_report,name='transaction_report'),
    path('reminder_report',views.reminder_report,name='reminder_report'),
    path('complaint_report',views.complaint_report,name='complaint_report'),
    path('payment_report',views.payment_report,name='payment_report'),
    path('registration_report',views.registration_report,name='registration_report'),

    path('locations',views.locations,name='locations'),


    

    
    



    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
