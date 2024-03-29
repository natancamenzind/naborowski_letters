# Generated by Django 4.1 on 2023-05-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0003_alter_text_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='content',
            field=models.TextField(default='', verbose_name='treść'),
        ),
        migrations.AddField(
            model_name='text',
            name='send_date',
            field=models.DateField(blank=True, null=True, verbose_name='data wysłania'),
        ),
    ]
