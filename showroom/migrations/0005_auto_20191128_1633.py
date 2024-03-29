# Generated by Django 2.0.3 on 2019-11-28 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showroom', '0004_auto_20191128_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saleproducts',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Sales Products'},
        ),
        migrations.RemoveField(
            model_name='saleproducts',
            name='per_installment_amount',
        ),
        migrations.AddField(
            model_name='saleproducts',
            name='next_installment_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='saleproducts',
            name='next_installment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
