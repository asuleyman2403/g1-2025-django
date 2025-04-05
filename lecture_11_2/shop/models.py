from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(null=False, max_length=255, blank=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'ID: {self.id} {self.name}'


class Product(models.Model):
    name = models.CharField(null=False, max_length=255, blank=False)
    description = models.CharField(null=False, max_length=2000, blank=True, default='')
    price = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'ID: {self.id} {self.name}'


class BasketItem(models.Model):
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, default=1)

    class Meta:
        verbose_name = 'Basket Item'
        verbose_name_plural = 'Basket Items'

    def __str__(self):
        return f'ID: {self.id} {self.product.name} {self.amount}'




