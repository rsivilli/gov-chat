# Generated by Django 4.2.3 on 2023-07-25 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management', '0005_remove_website_last_scanned_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='site_doc_staging',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]