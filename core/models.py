from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('COMPLETE', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    tracking_id = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=50)  
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PROCESSED')
    currency = models.CharField(max_length=10)  
    account = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.tracking_id} - {self.user} - {self.status}"

class WriterApplication(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    summary = models.TextField()
    portfolio = models.FileField(upload_to="portfolios/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Track approval status

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class WriterProfile(models.Model):
    avatar = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)
    specialization = models.CharField(max_length=255)
    skills = models.JSONField(default=list)  # Store skills as a list
    projects = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name        


class Review(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField()
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.title        