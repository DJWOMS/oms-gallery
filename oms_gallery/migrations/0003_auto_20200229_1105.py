# Generated by Django 3.0.3 on 2020-02-29 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oms_gallery', '0002_auto_20190714_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='captions',
            field=models.TextField(blank=True, verbose_name='Подпись'),
        ),
    ]
