# Generated by Django 2.2.3 on 2019-07-14 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oms_gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['name'], 'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
    ]
