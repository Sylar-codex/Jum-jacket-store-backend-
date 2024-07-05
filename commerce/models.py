from pyexpat import model
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
# from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Product(models.Model) :
    product_name=models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price_naira = models.IntegerField(default=0)
    price_dollar = models.IntegerField(default=0)
    count = models.IntegerField(default=1)
    image = models.ImageField(upload_to='products/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model) :
    product_name=models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price_naira = models.IntegerField(default=0)
    price_dollar = models.IntegerField(default=0)
    count = models.IntegerField(default=1)
    image = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name="carts" , on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class BillingForm(models.Model) :
    full_name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    home_address = models.CharField(max_length=500)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)

    def save(self, *args, **kwargs) :
        send_mail(
            'BillingForm',
            'Here are the details of your customer order',
            settings.EMAIL_HOST_USER,
            ['vicaremy@gmail.com'],
            fail_silently=False,
            html_message=f'<p>Buyer-name: {self.full_name}</p><p>Email: {self.email}</p><p>Address: {self.home_address}</p><p>City: {self.city}</p><p>State: {self.state}</p><p>Country: {self.country}</p><p>Phone-number: {self.phone}</p>'
        )
        return super(BillingForm,self).save(*args,**kwargs)

