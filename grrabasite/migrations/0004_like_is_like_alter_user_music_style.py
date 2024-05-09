# Generated by Django 5.0.3 on 2024-04-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grrabasite', '0003_musiccategory_alter_user_music_style_music_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='is_like',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='music_style',
            field=models.CharField(blank=True, choices=[('chanson', 'Шансон, романс, авторская песня'), ('country', 'Кантри'), ('blues', 'Блюз'), ('rnb', 'Ритм-н-блюз'), ('rap', 'репер'), ('jazz', 'Джаз'), ('folk', 'Фолк-музыка'), ('latin', 'Латиноамериканская музыка'), ('electronic', 'Электронная музыка')], max_length=50, null=True),
        ),
    ]