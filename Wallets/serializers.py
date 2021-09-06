import random
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
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    wallet = serializers.CharField(read_only=True)
    class Meta: 
        model = User
        fields = ('email', 'password', 'wallet',)

    def create_no(self):
        new_num = str(random.randint(7500000001, 7599999999))
        try:
            existing_num = Wallet.objects.get(account_no=new_num)
            return self.create_no()
        except:
            return new_num


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        wallet = Wallet.objects.create(owner=user, account_no=self.create_no())
        return {'email': user.email, 'wallet': wallet }

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
    recipient = serializers.EmailField(write_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True) 
    detail = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True) 
    status = serializers.CharField(read_only=True) 
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def transfer(self, sender, recipient, amount, detail):
        sending_wallet = Wallet.objects.get(owner=sender)
        get_user = get_object_or_404(User, email=recipient)
        recipient_wallet  = Wallet.objects.get(owner = get_user)
        if recipient_wallet == sending_wallet:
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
        
        sending_wallet.balance -= amount
        recipient_wallet.balance += amount
        sending_wallet.save()
        recipient_wallet.save()
        TransactionHistory.objects.create(sender=sending_wallet, trans_type=TransactionHistory.DEBIT, amount=amount, recipient=recipient_wallet, details=detail )
        TransactionHistory.objects.create(sender=sending_wallet, trans_type=TransactionHistory.CREDIT, amount=amount, recipient=recipient_wallet, details=detail )
        return {
            'status' : 'success',
            'message' : 'Transfer successful',
            'balance' : sending_wallet.balance
        }


    def validate(self, data):
        recipient = data.get("recipient", None)
        amount = data.get("amount", None)
        detail = data.get("detail", None)
        sender = self.context['request'].user
        transfer = self.transfer(sender, recipient, amount, detail)
        if transfer['status'] == 'success':
            return {
                'status' : transfer['status'],
                'message' : transfer['message'],
                'balance' : transfer['balance']
            }
        else:
            return  {
            'status' : transfer['status'],
            'message' : transfer['message']
            }


class FundWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    message = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True) 
    balance = serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)

    def fund_wallet(self, amount, recipient):
        recipient_wallet = Wallet.objects.get(owner=recipient)
        recipient_wallet.balance += amount
        recipient_wallet.save()
        TransactionHistory.objects.create(sender=recipient_wallet, trans_type=TransactionHistory.FUND_WALLET, amount=amount, recipient=recipient_wallet, details='Fund Wallet')
        return {
            'status' : 'success',
            'message' : 'Wallet Funded',
            'balance' : recipient_wallet.balance
        }

    def validate(self, data):
        amount = data.get("amount", None)
        recipient= self.context['request'].user
        payment = flutter_wave(amount, recipient.email)

        if payment["status"] == "error":
            return {
                'status': payment["status"],
                'message': payment["error"]["errMsg"] 
                }
        if payment["status"] == "success":
            amount = Decimal(payment["success"]["amount"])
            fund_wallet = self.fund_wallet(amount, recipient)
            return {  
                    'status' : 'success',
                    'message' : fund_wallet['message'], 
                    'balance' : fund_wallet['balance']
                }
            


class TransactionHistorySerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='account_no', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='account_no', read_only=True)
    class Meta:
        model = TransactionHistory
        fields = ('__all__')

