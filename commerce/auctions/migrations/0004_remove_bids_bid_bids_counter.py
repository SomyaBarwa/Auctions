# Generated by Django 4.2.1 on 2023-05-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listings_owner_alter_bids_bidder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='bid',
        ),
        migrations.AddField(
            model_name='bids',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
