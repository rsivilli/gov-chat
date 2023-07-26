from django.contrib import admin

# Register your models here.
from .models import Customer,Website, ChatbotConfig


class WebstesInline(admin.StackedInline):
    model = Website
    extra = 1
class chatbotInline(admin.StackedInline):
    model = ChatbotConfig
    extra = 1
class CustomerRegister(admin.ModelAdmin):
    inlines = [WebstesInline, chatbotInline]

admin.site.register(Customer,CustomerRegister)
