from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Product(models.Model):
    categories = (('Fashions', 'Fashions'),
                ('Electronics', 'Electronics'),
                ('Toys', 'Toys'),
                ('Home', 'Home'),
                )
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=200, choices=categories)
    price = models.IntegerField()
    image_link = models.CharField(max_length=200, null=True, blank=True, default=None)
    selled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    bidding = models.IntegerField()

    def __str__(self):
        return f" '{self.user_id}' : '{self.product_id}' to {self.bidding}$"

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_name')


    def __str__(self):
        return f"{self.user_id} : {self.product_id}"

class Result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    successful_bid = models.IntegerField()

    def __str__(self):
        return f" Product '{self.product_id}' s Winner : '{self.user_id}' "
