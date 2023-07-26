from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Customer

def index(request):
    latest_customers = Customer.objects.order_by("name")[:5]
    output = ",".join([c.name for c in latest_customers])
    return HttpResponse(output)
def detail(request, customer_id):
    return HttpResponse("You're looking at customer %s."%customer_id) 
