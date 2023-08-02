from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
default_template_prompt = (
        "Use the following pieces of context to answer the question at the end. "
        "If you don't know the answer, just say that you don't know, don't try to make up an answer. "
        "Use three sentences maximum and keep the answer as concise as possible. "
        "Always say \"thanks for asking!\" at the end of the answer.\n"
        "{context}\n"
        "Question: {question}\n"
        "Helpful Answer:"
    )
class Customer(models.Model):
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        return self.name
    name = models.CharField(max_length=200)


class VectorStoreCollection(models.Model):
    def __str__(self) -> str:
        return self.name
    
    name = models.CharField(max_length=100)

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
     target_collections =  models.ManyToManyField(VectorStoreCollection)
     def __repr__(self) -> str:
         return f"{self.customer.name}-{self.base_site}"
class SupportedModels(models.TextChoices):
    GPT4All_J_v1_3_groovy = "GPT4All-J v1.3-groovy"


class ChatbotConfig(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.CharField(max_length=100,choices=SupportedModels.choices,default=SupportedModels.GPT4All_J_v1_3_groovy)
    temperature = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],default=0
    )
    limit_time_seconds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3600)], default=60)
    limit_messages_per_time_per_device = models.IntegerField(validators=[MinValueValidator(0)],default=20)
    not_found_response = models.TextField(max_length=255,default="I'm sorry, I can't find information about your question")
    prompt_template = models.TextField(max_length=500, default=default_template_prompt, null= False, blank=False)
    default_collection = models.ForeignKey(VectorStoreCollection, blank= True, null=True, on_delete=models.SET_NULL)
    verbose = models.BooleanField(default=False, blank=False, null=False)
    return_source_documents = models.BooleanField(default=True, blank=False, null=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)