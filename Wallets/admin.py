from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Wallet, TransactionHistory

# Register your models here.
class TransactionHistoryAdmin(admin.ModelAdmin):
    readonly_fields=("reference_number", "trans_type", "sender", "recipient", "amount", "details", "time")
    list_display = ("reference_number", "trans_type", "sender", "recipient", "amount", "time")
    search_fields = ("trans_type", "sender__account_no", "sender__owner__email","recipient__account_no","recipient__owner__email", "amount")
    list_filter = ("trans_type",)
    list_per_page = 50

class WalletsAdmin(admin.ModelAdmin):
    readonly_fields=("account_no", "owner", "balance", "date_created", "date_modified")
    list_display = ("account_no", "owner", "balance")
    search_fields = ("account_no", "owner__email")
    list_per_page = 50

admin.site.register(User)
admin.site.register(Wallet, WalletsAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)

admin.site.unregister(Group)
