# Generated by Django 5.0 on 2024-01-19 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_fooditem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
