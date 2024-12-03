from django.contrib.auth.models import AbstractUser
from django.db import models
from admin_page.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    
    def __str__(self):
        return self.username

class Order(models.Model):
    PAYMENT_METHODS = [
        ('GCash', 'GCash'),
        ('PayPal', 'PayPal'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class CartItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # New status field

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.product.price

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='default_profile.png')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_customer(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customer'):
        Customer.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_customer(sender, instance, **kwargs):
    if hasattr(instance, 'customer'):
        instance.customer.save()

class ProductRating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)  # Use related_name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Ratings from 1 to 5
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating}'

    class Meta:
        unique_together = ('product', 'user')  # Ensures a user can rate a product only once
