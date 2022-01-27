from django.contrib import admin
from .models import *
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display=('user','image','user_type')
    
admin.site.register(Contact)
admin.site.register(Register,RegisterAdmin)
admin.site.register(MoneyTransfer)

admin.site.register(Complaint)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Reminder)

