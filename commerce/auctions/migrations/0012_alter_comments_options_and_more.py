# Generated by Django 4.2.1 on 2023-05-25 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_bids_bid_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['created_date']},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='commenter',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='date_commented',
            new_name='created_date',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='comment',
        ),
        migrations.AddField(
            model_name='comments',
            name='body',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
