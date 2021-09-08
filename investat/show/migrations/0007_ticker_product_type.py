# Generated by Django 3.2.7 on 2021-09-07 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0006_dividend'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='product_type',
            field=models.CharField(choices=[('ETF', 'Exchange-traded fund'), ('STO', 'Stock'), ('OTH', 'Others')], default='OTH', max_length=3),
        ),
    ]
