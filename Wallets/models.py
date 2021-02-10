import uuid, random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
TRANSACTION_TYPE = (
    ('credit', 'Credit'),
    ('debit', 'Debit')
)
def create_no():
    return str(random.randint(7500000001, 7599999999))
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email,  password, **extra_fields):
        '''
        Create and return a `User` with superuser (admin) permisissions.
        '''
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password, is_superuser=True)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return self.email
    
class Wallet(models.Model):
    account_no = models.CharField(max_length=10, blank=True, editable=False, unique=True, default=create_no())
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.account_no
    

class Transaction_History(models.Model):
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE)
    amount  = models.FloatField(default=0.0)
    time = models.DateField(auto_now_add=True)
    receiver_or_sender = models.CharField(max_length=255)
    details = models.CharField(max_length=255)

    def __str__(self):
        return str(self.reference_number)
    


