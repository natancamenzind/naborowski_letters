# Generated by Django 4.1.7 on 2023-05-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_alter_persontextappearance_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='persontextappearance',
            name='context',
            field=models.CharField(default='', max_length=500, verbose_name='kontekst wystąpienia'),
        ),
    ]
