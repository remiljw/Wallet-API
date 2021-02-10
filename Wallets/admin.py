from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Wallet, TransactionHistory

# Register your models here.

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(TransactionHistory)

admin.site.unregister(Group)
