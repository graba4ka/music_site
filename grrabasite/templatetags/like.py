from django import template

register = template.Library()


@register.inclusion_tag("grrabasite/partials/like.html", takes_context=True)
def like_btn(context, music):
    liked = context["request"].user.likes.filter(id=music.id).exists()
    return {"music": music, "liked": liked}