# Generated by Django 5.1.6 on 2025-03-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active')], default='pending', max_length=20)),
            ],
        ),
    ]
