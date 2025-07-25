# Generated by Django 5.2.4 on 2025-07-23 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalimage',
            name='general',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.general'),
        ),
        migrations.AlterField(
            model_name='helper',
            name='general',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='helper', to='blog.general'),
        ),
    ]
