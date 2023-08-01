from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(models.Model):
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        return self.name
    name = models.CharField(max_length=200)

class Website(models.Model):
     def __str__(self) -> str:
         return self.base_site
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     base_site = models.CharField(max_length=200,unique=True)
     site_map = models.CharField(max_length=200,null=True,default=None, blank=True )
     update_site_map = models.BooleanField(default=False, null=False, blank= False)
     create_site_map = models.BooleanField(default=False, null = False, blank=False)
     site_map_last_scanned = models.DateField(null= True, blank=True)
     site_last_indexed = models.DateField(null=True, blank=True)
     site_doc_staging = models.CharField(max_length=200,null=True,default=None, blank=True )
     site_collection_name = models.CharField(max_length=200,null=True, default=None,blank=True)
     def __repr__(self) -> str:
         return f"{self.customer.name}-{self.base_site}"
class SupportedModels(models.TextChoices):
    GPT4All_J_v1_3_groovy = "GPT4All-J v1.3-groovy"


class ChatbotConfig(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,unique=True)
    model = models.CharField(max_length=100,choices=SupportedModels.choices,default=SupportedModels.GPT4All_J_v1_3_groovy)
    temperature = models.FloatField(

        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],default=0)
    limit_time_seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3600)], default=60)
    limit_messages_per_time_per_device = models.IntegerField(validators=[MinValueValidator(0)],default=20)
    not_found_response = models.TextField(max_length=255,default="I'm sorry, I can't find information about your question")
    