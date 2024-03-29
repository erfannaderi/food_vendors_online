# Generated by Django 5.0 on 2024-01-29 13:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0003_tax_alter_discount_discount_percentage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='discount',
            name='maximum',
            field=models.DecimalField(decimal_places=2, default=800, max_digits=12),
        ),
        migrations.AddField(
            model_name='discount',
            name='minimum',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
        ),
        migrations.AlterField(
            model_name='discount',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
