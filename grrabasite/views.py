from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse
from django_filters.views import FilterView

from grrabasite.filters import MusicFilter
from .models import Music, MusicCategory, Review, User
from .forms import LoginForm, SignupForm, UploadSongForm


def main_page(request):
    return HttpResponse("успешная логинка и сигнап")


class SignupView(FormView):
    template_name = "grrabasite/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AuthenticationView(FormView):
    template_name = "grrabasite/signin.html"
    form_class = LoginForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)


class ProfileView(View):
    template_name = "grrabasite/profile.html"

    def get(self, request, *args, **kwargs):
        if 'username' in kwargs:
            user = get_object_or_404(User, name=kwargs['username'])
        else:
            user = request.user
        user_name = user.name
        user_music_style = user.music_style
        user_songs = user.uploaded_music.all()

        context = {
            "user_name": user_name,
            "user_music_style": user_music_style,
            "user_songs": user_songs,
        }
        

        return render(request, self.template_name, context=context)


def upload_song(request):
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            audio_file = form.cleaned_data['audio_file']
            category = form.cleaned_data['category']
            category_obj, created = MusicCategory.objects.get_or_create(name=category)
            music = Music(name=title, music_file=audio_file, author=request.user, category=category_obj)
            music.save()
            return redirect('main_page')
    else:
        form = UploadSongForm()
    return render(request, 'grrabasite/upload_song.html', {'form': form})


def save_music(request):
    if request.method == 'POST':
        if 'like_music_id' in request.POST:
            music_id = request.POST.get('like_music_id')
            music = get_object_or_404(Music, pk=music_id)
            request.user.likes.add(music)
            
        elif 'dislike_music_id' in request.POST:
            
            music_id = request.POST.get('dislike_music_id')
            music = get_object_or_404(Music, pk=music_id)
            request.user.likes.remove(music)
        request.user.save()

        
    return redirect('music_list')


def otzuv_music(request):
    if request.method == 'POST':
        music_id = request.POST.get('music_id')
        review_comment = request.POST.get('review')

        music = get_object_or_404(Music, pk=music_id)
        review = Review.objects.create(user=request.user, music=music, comment=review_comment)
        review.save()

    return redirect('music_list')


class MusicListView(FilterView):
    model = Music
    template_name = 'grrabasite/music_list.html'
    filterset_class = MusicFilter
    context_object_name = 'music_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music_list = context['music_list']
        paginator = Paginator(music_list, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            music = paginator.page(page)
        except PageNotAnInteger:
            music = paginator.page(1)
        except EmptyPage:
            music = paginator.page(paginator.num_pages)

        context['music_list'] = music
        user = self.request.user
        user_reviews = {music.id: Review.objects.filter(user=user, music=music) for music in music_list}
        context['user_reviews'] = user_reviews
        return context


def logout(request):
    auth_logout(request)
    return redirect('main_page')
