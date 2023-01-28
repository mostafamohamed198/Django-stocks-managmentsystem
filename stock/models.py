from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
# Create your models here.

class User(AbstractUser):
    pass


class types(models.Model):
    type = models.CharField(max_length=200)
    hiddenname = models.CharField(max_length=200, null=True, blank=True,default=None)

    def __str__(self):
        return str(self.type)

class stock(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    boughtprice =models.IntegerField()
    expectedexitprice = models.IntegerField()
    stocktype = models.ForeignKey('types', on_delete=models.CASCADE,default=None)
    timesubmitted = models.DateTimeField(auto_now_add=True)
    expectedtime = models.DateTimeField()
    start = models.DateField(default=None)
    end = models.DateField(default=None)

    def __str__(self):
        return '%s' % (self.name)


class watchlist(models.Model):
    name = models.CharField(max_length=200)
    stocks = models.ManyToManyField('stock', default=None, null=True, blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)

class news(models.Model):
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    relatedstock = models.ForeignKey('stock',on_delete=models.CASCADE,default=None)