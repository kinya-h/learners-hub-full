from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('COMPLETED', 'success'),
        ('FAILED', 'failed'),
        ('REVERSED', 'reversed'),
        ('PROCESSED', 'processing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    paystack_reference = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PROCESSED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paystack_reference} - {self.amount} USD"
