# Generated by Django 4.2.3 on 2023-07-26 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management', '0007_chatbotconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotconfig',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer_management.customer'),
        ),
    ]