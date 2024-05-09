from django.urls import path
from django.contrib.auth.decorators import login_required
from grrabasite.views import AuthenticationView, SignupView, main_page, ProfileView, otzuv_music, save_music, upload_song, MusicListView, logout

urlpatterns = [
    path("good/", main_page, name="main_page"),  # Для главной страницы
    path("signup/", SignupView.as_view(), name="signup"),  # Для страницы регистрации
    path("signin/", AuthenticationView.as_view(), name="login"),  # Для страницы входа
    path("logout/", logout, name="logout"),  # Для выхода из системы
    path("profile/", login_required(ProfileView.as_view()), name="myprofile"),  # Для страницы профиля, требуется вход
    path("profile/<path:username>/", login_required(ProfileView.as_view()), name="profile"),
    path('upload/', login_required(upload_song), name='upload_song'),  # Для загрузки песни, требуется вход
    path('music/', login_required(MusicListView.as_view()), name='music_list'),  # Для списка музыки, требуется вход
    path('save_music/', login_required(save_music), name='save_music'),  # Для сохранения музыки (лайки/дизлайки), требуется вход
    path('otzuv_music/', login_required(otzuv_music), name='otzuv_music'),
]
