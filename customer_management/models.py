from django.db import models
import datetime

class Customer(models.Model):
    name = models.CharField(max_length=200)

class Website(models.Model):
     customer = models.ManyToManyField(Customer)
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     base_site = models.CharField(max_length=200,unique=True)
     site_map = models.CharField(max_length=200,null=True,default=None, blank=True )
     update_site_map = models.BooleanField(default=False, null=False, blank= False)
     create_site_map = models.BooleanField(default=False, null = False, blank=False)
     site_map_last_scanned = models.DateField(null= True, blank=True)
     site_last_indexed = models.DateField(null=True, blank=True)
     site_doc_staging = models.CharField(max_length=200,null=True,default=None, blank=True )
