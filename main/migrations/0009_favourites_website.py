# Generated by Django 3.0.8 on 2020-09-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200922_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourites',
            name='website',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
