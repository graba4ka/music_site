

from django.conf import settings
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _

from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self,
        name,
        email,
        music_style,
        password=None,
    ) -> "User":
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            music_style=music_style
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        name,
        email,
        music_style,
        password,
    ) -> "User":
        user = self.create_user(
            name=name,
            email=email,
            music_style=music_style,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save()
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)




class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_(" name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    music_style = models.CharField(
        max_length=50,
        choices={
            ("folk", "Фолк-музыка"),
            ("country", "Кантри"),
            ("latin", "Латиноамериканская музыка"),
            ("blues", "Блюз"),
            ("rnb", "Ритм-н-блюз"),
            ("jazz", "Джаз"),
            ("chanson", "Шансон, романс, авторская песня"),
            ("electronic", "Электронная музыка"),
            ("rap", "репер"),
        },
        null=True,
        blank=True,)
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "music_style",
    ]


# class Music(models.Model):
#     name = models.CharField(max_length=255)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_music')
#     music_file = models.FileField(upload_to='music/')

class Music(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_music')
    music_file = models.FileField(upload_to='music/')
    likes =  models.ManyToManyField(settings.AUTH_USER_MODEL, through="Like", through_fields=("music", "user"), related_name="likes")
    category = models.ForeignKey("MusicCategory", related_name="music", on_delete=models.CASCADE, null=True)
    
    @property
    def total_likes(self):
        return self.likes.count()
    

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes_set')
    music = models.ForeignKey('Music', on_delete=models.CASCADE, related_name='likes_set')

    class Meta:
        unique_together = ('user', 'music')



class MusicCategory(models.Model):
    name = models.CharField(max_length=32)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    music = models.ForeignKey('Music', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.name} on {self.music.name}"