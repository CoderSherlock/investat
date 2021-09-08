# Generated by Django 3.2.7 on 2021-09-07 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0007_ticker_product_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brokerage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brokerage_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='ticker',
            name='operator_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='show.operator'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='show.brokerage'),
        ),
    ]
