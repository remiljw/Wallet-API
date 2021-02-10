from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import SignUpView, FundWalletView, P2PTransferView, CreateWalletView, GetTransactionHistoryView 

app_name = 'Wallets'

urlpatterns = [
     path('signup/', SignUpView.as_view()),
     path('get-token/', obtain_jwt_token),
     path('transfer/', P2PTransferView.as_view()), 
     path('create-wallet/', CreateWalletView.as_view()),
     path('transactions/', GetTransactionHistoryView.as_view()),
     path('fund-wallet/', FundWalletView.as_view())
]
