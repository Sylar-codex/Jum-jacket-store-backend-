from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Wallet(models.Model) :
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.user.__str__()

class WalletTransaction(models.Model) :
    TRANSACTIONS_TYPES = (
        ('deposit','deposit'),
        ('transfer','transfer'),
        ('withdraw','withdraw'),
    )

    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=200, null=True, choices= TRANSACTIONS_TYPES)
    amount = models.DecimalField(max_digits=70,null=True, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=100, default= "pending")
    paystack_payment_ref = models.CharField(max_length=100, default='', blank=True)

    def __str__(self) :
        return self.wallet.user.__str__()
    
class WalletTransactionStripe(models.Model) :
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=100, default='', blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    amount = models.DecimalField(max_digits=70,null=True, decimal_places=2)
