# Generated by Django 4.2 on 2023-04-11 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterintake',
            name='intake',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]