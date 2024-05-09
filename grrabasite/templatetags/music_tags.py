from django import template

register = template.Library()

@register.simple_tag
def get_reviews_for_music(music, user_reviews):
    reviews_for_music = user_reviews.get(music.id, [])
    return reviews_for_music
