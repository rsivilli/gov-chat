# Generated by Django 4.2.3 on 2023-07-27 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management', '0008_alter_chatbotconfig_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotconfig',
            name='collection_name',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]