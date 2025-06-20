# Generated by Django 4.2.3 on 2025-06-09 10:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('triblinbackend', '0016_remove_location_user_delete_location_count_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('location_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='location_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100)),
                ('location_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Plastic_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('plastic_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('location_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='Plastic_Item_Replacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replacement_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('replaced_with', models.CharField(max_length=100)),
                ('disposed_type', models.CharField(max_length=100)),
                ('location_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.location')),
                ('plastic_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.plastic_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triblinbackend.authuser')),
            ],
        ),
    ]
