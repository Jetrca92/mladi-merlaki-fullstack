# Generated by Django 5.0.2 on 2024-03-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketdata', '0003_alter_stock_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='dividend',
            field=models.FloatField(null=True),
        ),
    ]
