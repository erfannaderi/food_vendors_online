# Generated by Django 5.0 on 2023-12-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=60)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=14)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'RESTAURANT'), (2, 'CLIENT')], null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
