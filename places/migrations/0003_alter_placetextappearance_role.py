# Generated by Django 4.1.7 on 2023-05-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_alter_placetextappearance_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placetextappearance',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(0, 'wysłane z'), (1, 'odebrane w'), (2, 'wspomninie')]),
        ),
    ]
