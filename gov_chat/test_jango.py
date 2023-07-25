import django


import os
from gov_chat_management.gov_chat_management import settings as app_settings
from django.conf import settings

# settings.configure(default_settings=app_settings)
os.environ['DJANGO_SETTINGS_MODULE']= 'gov_chat_management.gov_chat_management.settings'
django.setup()


from gov_chat_management.customer_management.models import Customer


print(Customer.objects)