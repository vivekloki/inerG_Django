# Generated by Django 5.0.3 on 2024-03-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_well_number', models.IntegerField(null=True, unique=True)),
                ('oil', models.IntegerField(null=True)),
                ('gas', models.IntegerField(null=True)),
                ('brine', models.IntegerField(null=True)),
            ],
        ),
    ]
