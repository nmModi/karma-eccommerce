# Generated by Django 4.0.6 on 2022-07-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_detail',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
