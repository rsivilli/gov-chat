from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.template import loader


from .models import Customer

def index(request):
    latest_customers = Customer.objects.order_by("name")[:5]
    context = {
        "customer_list": latest_customers,
    }
    return render( request, "customer/index.html", context)


def detail(request, customer_id):
    customer = get_object_or_404(Customer,pk=customer_id)
    return render(request,"customer/detail.html",{"customer":customer})
