import django_filters
from .models import Music

class MusicFilter(django_filters.FilterSet):
    class Meta:
        model = Music
        fields = ['name', 'author__name', 'author__music_style']
    