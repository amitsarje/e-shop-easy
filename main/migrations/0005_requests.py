# Generated by Django 3.0.8 on 2020-09-22 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200922_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestedmoney', models.FloatField()),
                ('requester', models.IntegerField()),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Account')),
            ],
        ),
    ]