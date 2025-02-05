from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('COMPLETE', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed'),
        ('PROCESSED', 'Processing'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    tracking_id = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=50)  
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PROCESSED')
    paystack_reference = models.CharField(max_length=200, unique=True)
    currency = models.CharField(max_length=10)  
    account = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.tracking_id} - {self.user} - {self.state}"