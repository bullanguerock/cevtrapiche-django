# Generated by Django 4.0.1 on 2022-01-16 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='flow_token',
        ),
    ]
