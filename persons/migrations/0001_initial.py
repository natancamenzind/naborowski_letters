# Generated by Django 4.1.3 on 2022-11-13 19:50

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='klucz')),
                ('first_name', models.CharField(max_length=50, verbose_name='imie')),
                ('last_name', models.CharField(max_length=50, verbose_name='naziwsko')),
                ('date_of_birth_start', models.DateField(blank=True, null=True, verbose_name='data narodzin, początek')),
                ('date_of_birth_end', models.DateField(blank=True, null=True, verbose_name='data narodzin, koniec')),
                ('date_of_death_start', models.DateField(blank=True, null=True, verbose_name='data śmierci, początek')),
                ('date_of_death_end', models.DateField(blank=True, null=True, verbose_name='data śmierci, koniec')),
                ('life_range_display', models.CharField(blank=True, default='', max_length=50, verbose_name='zakres dat życia')),
                ('description', models.TextField(blank=True, default='', verbose_name='opis')),
                ('altered_names', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='inne imiona')),
            ],
            options={
                'verbose_name': 'Osoba',
                'verbose_name_plural': 'Osoby',
            },
        ),
    ]