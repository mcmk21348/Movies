# Generated by Django 3.0.7 on 2020-06-17 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20200616_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='фильмы'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='serial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Serials', verbose_name='Сериалы'),
        ),
    ]