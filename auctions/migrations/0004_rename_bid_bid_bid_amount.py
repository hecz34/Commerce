# Generated by Django 5.0.3 on 2024-05-31 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid',
            new_name='bid_amount',
        ),
    ]
