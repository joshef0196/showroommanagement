# Generated by Django 2.0.3 on 2019-11-28 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0005_auto_20191128_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='installmentcollection',
            name='invoice',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='saleproducts',
            name='invoice',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
