# Generated by Django 4.2.1 on 2023-05-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bids_bid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bid_date',
            field=models.DateTimeField(default=None),
        ),
    ]
