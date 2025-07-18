# Generated by Django 5.1.7 on 2025-03-24 09:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField()),
                ('reservation_time', models.TimeField()),
                ('number_of_guests', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('special_request', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.table')),
            ],
            options={
                'ordering': ['-reservation_date', '-reservation_time'],
            },
        ),
    ]
