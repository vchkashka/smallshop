# Generated by Django 4.2.1 on 2025-04-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
    ]
