# Generated by Django 4.1.7 on 2023-03-05 10:27

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('texts', '0003_alter_text_language'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='klucz')),
                ('geonames_reference', models.URLField(blank=True, null=True, verbose_name='odnośnik do geonames')),
                ('altered_names', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='występuje jako')),
            ],
            options={
                'verbose_name': 'Miejsce',
                'verbose_name_plural': 'Miejsca',
            },
        ),
        migrations.CreateModel(
            name='PlaceTextAppearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.PositiveSmallIntegerField(choices=[(0, 'wyzłane z'), (1, 'odebrane w'), (2, 'wspomninie')])),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_appearances', to='places.place', verbose_name='osoba')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appearing_places', to='texts.text', verbose_name='tekst')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='appearance',
            field=models.ManyToManyField(through='places.PlaceTextAppearance', to='texts.text'),
        ),
    ]
