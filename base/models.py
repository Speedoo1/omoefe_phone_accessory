import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Others'),

    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, null=True, choices=CHOICES)
    image = models.ImageField(blank=True, null=True, )
    address = models.CharField(max_length=5000, blank=True, null=True, )

    about_me = RichTextUploadingField(blank=True, null=True, )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class brand(models.Model):
    brand_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.brand_name)


class phone(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    former_price = models.IntegerField(null=True, blank=True)
    current_price = models.IntegerField(null=True, blank=True)
    product_description = RichTextUploadingField(null=True, blank=True)
    ram = models.CharField(max_length=100, null=True, blank=True)
    rom = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)

    Total_sold = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    current_price = models.IntegerField(null=True, blank=True)
    good_item = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=500)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class orders(models.Model):
    CHOICES = (
        ('delivered', 'Delivered'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),

    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=500)
    quantity = models.IntegerField()
    status = models.CharField(max_length=300, choices=CHOICES)
