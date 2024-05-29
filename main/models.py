from django.db import models
from django.contrib.auth.models import User
from django.forms import forms


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Market(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField()

    class Meta:
        db_table = 'markets'

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name

    def human_price(self):
        # Ваша реализация замены запятой в цене, если это необходимо
        return self.price.replace(',', ' ')

    class Meta:
        db_table = 'products'


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

class Model(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'models'
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class Storage(models.Model):
    size = models.IntegerField()

    class Meta:
        db_table = 'storage'
    def __str__(self):
        return str(self.size)

class SellerProduct(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'seller_products'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('SellerProduct', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Товар {self.product.id} в корзине"
    class Meta:
        db_table = 'cart_item'



class Smartphones(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    size = models.ForeignKey(Storage, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.CharField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.size}, {self.color})"

    class Meta:
        db_table = 'smartphones'

class MarketProduct(models.Model):
    id = models.AutoField(primary_key=True)
    smartphone = models.ForeignKey(Smartphones, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateTimeField()
    market_id = models.IntegerField()
    url = models.URLField()
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class Meta:
        db_table = 'market_products'

class PriceHistory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color_history')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='storage_history')
    price = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = 'price_history'
        ordering = ['date']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite: {self.model.model} by {self.user.username}"

    class Meta:
        db_table = 'favorites'
