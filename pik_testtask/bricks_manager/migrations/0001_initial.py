# Generated by Django 3.0.3 on 2020-02-26 19:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('construction_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Bricklaying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bricks_manager.Building')),
            ],
        ),
    ]