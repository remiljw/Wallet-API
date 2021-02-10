from rest_framework import serializers
from .models import User, Wallet, Transaction_History

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password' : {'write_only' : True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

class CreateWalletSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    # balance = serializers.SlugField(default=0.0)
    class Meta:
        model = Wallet
        fields = ('owner',)

        # def create(self, validated_data):
        #     new_wallet = Wallet.objects.get_or_create(**validated_data)
        #     return new_wallet


class P2PTransferSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=10, write_only=True)
    amount = serializers.FloatField(write_only=True) 
    detail = serializers.CharField(max_length=255, write_only=True)
    sender = serializers.CharField(max_length=255, read_only=True)
    message = serializers.CharField(read_only=True) 

    def transfer(self, sender, receiver, amount, detail):
        money =  float(amount)
        sending = Wallet.objects.get(owner = sender)
        receiving  = Wallet.objects.get(account_no= receiver)
        if money > sending.balance:
            return "You do not have enough balance to perform this transaction"
        else:
            sending.balance = float("%f" % (sending.balance - money))
            receiving.balance = float("%f" % (receiving.balance + money))
            sending.save()
            receiving.save()
            Transaction_History.objects.create(source=sending, trans_type='debit', amount=money, receiver_or_sender=receiving, details=detail )
            Transaction_History.objects.create(source=receiving, trans_type='credit', amount=money, receiver_or_sender=sending, details=detail )
            return "Transfer Successful"


    def validate(self, data):
        receiver = data.get("receiver", None)
        amount = data.get("amount", None)
        detail = data.get("detail", None)
        sender = self.context['request'].user

        return {
            'message' : self.transfer(sender, receiver, amount, detail)
            }


        
        

class FundWallet(serializers.Serializer):
    receiver = serializers.CharField(max_length=10)
    amount = serializers.FloatField()

    # def validate(self, data):



class TransactionHistorySerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='account_no', read_only=True)
    class Meta:
        model = Transaction_History
        fields = ('__all__')

class FundWalletSerializer(serializers.Serializer):
    pass