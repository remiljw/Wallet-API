from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import TransactionHistory, Wallet
from .serializers import P2PTransferSerializer, SignUpSerializer, \
    TransactionHistorySerializer, FundWalletSerializer, UserLoginSerializer
from django.http import JsonResponse


# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class P2PTransferView(APIView):
    serializer_class = P2PTransferSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if serializer.data['status'] == 'error':
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

class GetTransactionHistoryView(ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        user = Wallet.objects.get(owner=self.request.user)

        history = TransactionHistory.objects.filter((Q(sender=user) & (Q(trans_type=TransactionHistory.DEBIT) | Q(trans_type=TransactionHistory.FUND_WALLET))) 
            | (Q(recipient=user) & Q(trans_type=TransactionHistory.CREDIT)))
        return history.order_by('-time')

class FundWalletView(APIView):
    serializer_class = FundWalletSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if serializer.data['status'] == 'error':
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
