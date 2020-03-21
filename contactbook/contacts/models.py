from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class Contact_Event(models.Model):
    contact_A = models.ForeignKey(Contact, on_delete=models.CASCADE)
    contact_B = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateField()
