# Generated by Django 5.0 on 2023-12-28 08:27

import django.db.models.deletion
from django.conf import settings
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
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='user/profile_picture')),
                ('cover_photos', models.ImageField(blank=True, null=True, upload_to='user/cover_photos')),
                ('address_line1', models.TextField(blank=True, null=True)),
                ('address_line2', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
