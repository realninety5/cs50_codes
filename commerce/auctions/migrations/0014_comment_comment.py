# Generated by Django 3.1.5 on 2021-02-03 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]