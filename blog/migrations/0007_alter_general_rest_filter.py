# Generated by Django 5.2.1 on 2025-07-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_general_rest_filter_general_rest_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general',
            name='rest_filter',
            field=models.ManyToManyField(blank=True, null=True, related_name='restaurants', to='blog.restaurantfilter'),
        ),
    ]
