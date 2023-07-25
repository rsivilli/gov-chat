from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)

class Website(models.Model):
     customer = models.ManyToManyField(Customer)
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     base_site = models.CharField(max_length=200,unique=True)
     site_map = models.CharField(max_length=200,null=True,default=None, blank=True )

class Sitemap(models.Model):
     base_site = models.ForeignKey(Website, on_delete=models.CASCADE)
     route = models.TextField()
     last_updated = models.DateTimeField(null=True, blank=True)