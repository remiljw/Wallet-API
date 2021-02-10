from django.urls import path
from .views import SignUpView, FundWalletView, P2PTransferView, GetTransactionHistoryView, UserLoginView

app_name = 'Wallets'

urlpatterns = [
     path('signup/', SignUpView.as_view()),
     path('signin/', UserLoginView.as_view()),
     path('transfer/', P2PTransferView.as_view()), 
     path('transactions/', GetTransactionHistoryView.as_view()),
     path('fund-wallet/', FundWalletView.as_view())
]
