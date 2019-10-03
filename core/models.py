from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
