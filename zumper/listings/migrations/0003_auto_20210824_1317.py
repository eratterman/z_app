# Generated by Django 3.2.6 on 2021-08-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_alter_listing_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='cost',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='listing',
            name='num_bathrooms',
            field=models.CharField(max_length=20),
        ),
    ]