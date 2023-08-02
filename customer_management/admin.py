from django.contrib import admin

# Register your models here.
from .models import Customer,Website, ChatbotConfig, VectorStoreCollection
import logging

logger = logging.getLogger(__name__)


# see https://stackoverflow.com/questions/20833638/how-to-log-all-django-form-validation-errors
class LoggingMixin(object):
    def add_error(self, field, error):
        if field:
            logger.info('Form error on field %s: %s', field, error)
        else:
            logger.info('Form error: %s', error)
        super().add_error(field, error)

class CollectionsInLine(admin.StackedInline):
    model = Website.target_collections.through
    min_num = 1
    extra =1 
class WebstesInline(admin.StackedInline):
    model = Website
    extra = 1
    inlines = [CollectionsInLine]
class ChatbotInline(admin.StackedInline):
    model = ChatbotConfig
    extra = 1

    
class CustomerRegister(LoggingMixin,admin.ModelAdmin):
    inlines = [WebstesInline, ChatbotInline]

admin.site.register(Customer,CustomerRegister)
admin.site.register(VectorStoreCollection)
