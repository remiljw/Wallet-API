from rest_framework import serializers
from .payments import flutter_wave
from django.contrib.auth.models import update_last_login
from .models import Wallet, TransactionHistory
from django.contrib.auth import get_user_model, authenticate
from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404
from decimal import Decimal

User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # Ensure passwords are at least 8 characters long, no longer than 128 characters, and can not be read by the client.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    wallet = serializers.CharField(read_only=True)
    class Meta: 
        model = User
        fields = ('email', 'password', 'wallet',)
        

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        wallet = Wallet.objects.create(owner=user)
        return {
            'email' : user.email,
            'wallet' : wallet
        }

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }

class P2PTransferSerializer(serializers.Serializer):
    receiver = serializers.EmailField(write_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True) 
    detail = serializers.CharField(write_only=True)
    sender = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True) 
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def transfer(self, sender, receiver, amount, detail):
        sending_wallet = Wallet.objects.get(owner=sender)
        get_user = get_object_or_404(User, email=receiver)
        receiving_wallet  = Wallet.objects.get(owner = get_user)
        if receiving_wallet == sending_wallet:
            return { 
                'status' : 'error',
                'message' : 'You cannot transfer money to your self',
                }
        if amount > sending_wallet.balance:
            return {
                'status' : 'error',
                'message' : 'You do not have enough balance to perform this transaction',
                }
        if amount <= 0:
            return {
                'status' : 'error',
                'message' : 'Enter a Valid Amount',
                }
        sending_wallet.balance =(sending_wallet.balance - amount)
        receiving_wallet.balance = (receiving_wallet.balance + amount)
        sending_wallet.save()
        receiving_wallet.save()
        TransactionHistory.objects.create(source=sending_wallet, trans_type='debit', amount=amount, receiver_or_sender=receiving_wallet.owner, details=detail )
        TransactionHistory.objects.create(source=receiving_wallet, trans_type='credit', amount=amount, receiver_or_sender=sending_wallet.owner, details=detail )
        return {
            'status' : 'success',
            'message' : 'Transfer successful',
            'balance' : sending_wallet.balance
        }


    def validate(self, data):
        receiver = data.get("receiver", None)
        amount = data.get("amount", None)
        detail = data.get("detail", None)
        sender = self.context['request'].user
        transfer = self.transfer(sender, receiver, amount, detail)
        if transfer['status'] == 'success':
            return {
                'message' : transfer['message'],
                'balance' : transfer['balance']
            }
        else:
            return  {
            'message' : transfer['message'],
            }


class FundWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    receiver = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)

    def fund_wallet(self, amount, receiver):
        receiving_wallet = Wallet.objects.get(owner=receiver)
        receiving_wallet.balance = (receiving_wallet.balance + amount)
        receiving_wallet.save()
        TransactionHistory.objects.create(source=receiving_wallet, trans_type='fund_wallet', amount=amount, receiver_or_sender=receiving_wallet.owner, details='Fund Wallet')
        return {
            'message' : 'Wallet Funded',
            'balance' : receiving_wallet.balance
        }

    def validate(self, data):
        amount = data.get("amount", None)
        receiver = self.context['request'].user
        payment = flutter_wave(amount, receiver.email)

        if payment["status"] == "error":
            return {
                'message': payment["error"]["errMsg"] 
                }
        if payment["status"] == "success":
            amount = Decimal(payment["success"]["amount"])
            fund_wallet = self.fund_wallet(amount, receiver)
            return {  
                    'message' : fund_wallet['message'], 
                    'balance' : fund_wallet['balance']
                }
            


class TransactionHistorySerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='account_no', read_only=True)
    class Meta:
        model = TransactionHistory
        fields = ('__all__')

