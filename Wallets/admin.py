from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Wallet, Transaction_History

# Register your models here.

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Transaction_History)

admin.site.unregister(Group)
