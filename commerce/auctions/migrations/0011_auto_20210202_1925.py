# Generated by Django 3.1.5 on 2021-02-02 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='status',
            new_name='active',
        ),
    ]
