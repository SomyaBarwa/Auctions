# Generated by Django 4.2.1 on 2023-05-25 11:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bids_bid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bid_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]