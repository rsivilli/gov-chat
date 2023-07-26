from django.contrib import admin

# Register your models here.
from .models import Customer,Website


class WebstesInline(admin.StackedInline):
    model = Website
    extra = 1
class CustomerRegister(admin.ModelAdmin):
    inlines = [WebstesInline]

admin.site.register(Customer,CustomerRegister)
