# Generated by Django 4.0.1 on 2022-02-14 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_collector', '0002_invoice_delete_billitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='outcome',
            field=models.BooleanField(default=False),
        ),
    ]