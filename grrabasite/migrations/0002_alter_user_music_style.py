# Generated by Django 5.0.3 on 2024-04-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grrabasite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='music_style',
            field=models.CharField(blank=True, choices=[('rap', 'репер'), ('folk', 'Фолк-музыка'), ('jazz', 'Джаз'), ('blues', 'Блюз'), ('electronic', 'Электронная музыка'), ('rnb', 'Ритм-н-блюз'), ('chanson', 'Шансон, романс, авторская песня'), ('country', 'Кантри'), ('latin', 'Латиноамериканская музыка')], max_length=50, null=True),
        ),
    ]
