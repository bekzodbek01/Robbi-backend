# Generated by Django 5.2.1 on 2025-07-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_general_category_alter_general_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='general',
            name='rest_filter',
        ),
        migrations.AddField(
            model_name='general',
            name='rest_filter',
            field=models.ManyToManyField(blank=True, related_name='restaurants', to='blog.restaurantfilter'),
        ),
    ]
