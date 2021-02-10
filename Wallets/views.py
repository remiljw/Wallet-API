from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import User, Wallet, TransactionHistory
from .serializers import P2PTransferSerializer, SignUpSerializer, TransactionHistorySerializer, FundWalletSerializer, UserLoginSerializer


# Create your views here.

class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLoginView(RetrieveAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        pass

    def get_object(self):
        pass

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

class P2PTransferView(CreateAPIView):
    serializer_class = P2PTransferSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

class GetTransactionHistoryView(ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        history = TransactionHistory.objects.filter(source=self.request.user.wallet)
        return history.order_by('-time')

class FundWalletView(CreateAPIView):
    serializer_class = FundWalletSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)