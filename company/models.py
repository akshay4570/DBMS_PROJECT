from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=25, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    price = models.IntegerField()
    image = models.ImageField(upload_to='company/images', default="")
    quantity = models.IntegerField()
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE,)
    comp_id = models.ForeignKey('Company', on_delete=models.CASCADE,)

    def __str__(self):
        return self.name