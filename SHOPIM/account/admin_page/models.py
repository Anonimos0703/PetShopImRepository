from django.db import models

# Create your models here.
from django.db import models

CATEGORY = (
    ('Food', 'Food'),
    ('Toys', 'Toys'),
    ('Fur Clothing', 'Fur Clothing'),
    ('Care Products', 'Care Products'),
)

class Inventory(models.Model):
    inventoryId = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.inventoryId}'

    
class Product(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    price = models.PositiveBigIntegerField(null=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    def average_rating(self):
        ratings = self.productrating_set.all()  # Use the reverse relationship
        return sum(rating.rating for rating in ratings) / ratings.count() if ratings.exists() else 0
    
    def reduce_quantity(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
            return True
        return False
    

