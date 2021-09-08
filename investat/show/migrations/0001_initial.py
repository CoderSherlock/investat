# Generated by Django 3.2.7 on 2021-09-07 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tran_date', models.DateField(verbose_name='transaction date')),
                ('ticker', models.CharField(max_length=20)),
                ('price', models.FloatField()),
            ],
        ),
    ]
