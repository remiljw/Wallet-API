from django.urls import path
from .views import SignUpView, FundWalletView, P2PTransferView, GetTransactionHistoryView, UserLoginView

app_name = 'Wallets'

urlpatterns = [
     path('signup', SignUpView.as_view(), name='signup'),
     path('signin', UserLoginView.as_view(), name='sigin'),
     path('transfer', P2PTransferView.as_view(), name='transfers'), 
     path('transactions', GetTransactionHistoryView.as_view(), name='transactionhistory-detail'),
     path('fund-wallet', FundWalletView.as_view(), name='fundwallet')
]
