from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from .models import Wallet, Transaction_History
from django.contrib.auth import get_user_model, authenticate
from rest_framework_jwt.settings import api_settings

User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class SignUpSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password' : {'write_only' : True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            wallet = Wallet.objects.create(owner=user)
            return { 'user': user, 'wallet': wallet}

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
    amount = serializers.FloatField(write_only=True) 
    detail = serializers.CharField(write_only=True)
    sender = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True) 

    def transfer(self, sender, receiver, amount, detail):
        money =  amount
        sending = Wallet.objects.get(owner = sender)
        rec_user = User.objects.get(email=receiver)
        receiving  = Wallet.objects.get(owner = rec_user)
        if receiving == sending:
            return "You cannot transfer money to your self"
        if money > sending.balance:
            return "You do not have enough balance to perform this transaction"
        else:
            sending.balance = float("%f" % (sending.balance - money))
            receiving.balance = float("%f" % (receiving.balance + money))
            sending.save()
            receiving.save()
            Transaction_History.objects.create(source=sending, trans_type='debit', amount=money, receiver_or_sender=receiving.owner, details=detail )
            Transaction_History.objects.create(source=receiving, trans_type='credit', amount=money, receiver_or_sender=sending.owner, details=detail )
            return "Transfer Successful"


    def validate(self, data):
        receiver = data.get("receiver", None)
        amount = data.get("amount", None)
        detail = data.get("detail", None)
        sender = self.context['request'].user
        
        return {
            'message' : self.transfer(sender, receiver, amount, detail)
            }


class FundWalletSerializer(serializers.Serializer):
    amount = serializers.FloatField(write_only=True)
    sender = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)

    def fund_wallet(self, amount, sender):
        money = amount
        sending = Wallet.objects.get(owner = sender)
        sending.balance = float("%f" % (sending.balance + money))
        sending.save()
        Transaction_History.objects.create(source=sending, trans_type='fund_wallet', amount=money, receiver_or_sender=sending.owner, details='Fund Wallet')
        return "Wallet Funded"

    def validate(self, data):
        amount = data.get("amount", None)
        sender = self.context['request'].user
        return {
            'message' : self.fund_wallet(amount, sender)
        }


class TransactionHistorySerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='account_no', read_only=True)
    class Meta:
        model = Transaction_History
        fields = ('__all__')

