from django.db import models


# Create your models here.
class Customer(models.Model):
    id = models.AutoField
    username = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    password = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ecom/images', default="")

    def __str__(self):
        return self.username


class Shipping(models.Model):
    sid = models.AutoField(primary_key=True)
    cid = models.ForeignKey('Customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    phone = models.BigIntegerField()

    def __str__(self):
        return str(self.sid)


class Order(models.Model):
    id = models.AutoField
    cid = models.ForeignKey('Customer', on_delete=models.CASCADE)
    sid = models.ForeignKey('Shipping', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    prods = models.CharField(max_length=1000, default='')

    def __str__(self):
        return str(self.id)