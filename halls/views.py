from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from .models import Hall, Video
from .forms import HallForm, AddVideoForm, SearchForm
from .mixins import AddVideoMixin
from urllib.parse import urlparse
import requests

YOUTUBE_API_KEY = 'AIzaSyDd_yJ-TyaWGzGNN0DyAC3rZPy9izKkjmQ'


def home(request):
    return render(request, 'halls/home.html')


def dashboard(request):
    return render(request, 'halls/dashboard.html')


def video_search(request):
    search_term = request.GET['search_term']
    return JsonResponse({'search_term': search_term})


class AddVideo(AddVideoMixin, generic.FormView):
    form_class = AddVideoForm
    template_name = 'halls/addvideo.html'

    def get(self, request, *args, **kwargs):
        hall = Hall.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.username != hall.user.username:
            raise Http404()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hall'] = Hall.objects.get(**self.kwargs)
        return context


class DeleteVideo(generic.DeleteView):
    model = Video
    template_name = 'halls/deletevideo.html'


@method_decorator(login_required, name='dispatch')
class Dashboard(generic.ListView):
    model = Hall
    template_name = 'halls/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halls'] = self.model.objects.filter(user=self.request.user)
        return context


def create_hall(request):

    if request.method == 'GET':
        form = HallForm()
        return render(request, 'halls/createhall.html', {'form': form})

    form = HallForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        hall = Hall()
        hall.title = title
        hall.user = request.user
        hall.save()
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class CreateHall(generic.CreateView):
    model = Hall
    fields = ['title']
    http_method_names = ['get', 'post']
    initial = {'title': ''}
    template_name = 'halls/createhall.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('detailhall', kwargs=self.kwargs)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('detailhall', kwargs={'pk': pk})


class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detailhall.html'


@method_decorator(login_required, name='dispatch')
class UpdateHall(generic.UpdateView):
    model = Hall
    template_name = 'halls/updatehall.html'
    fields = ['title']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.success_url = reverse_lazy('detailhall', kwargs=self.kwargs)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = 'halls/deletehall.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hall'] = self.object.title
        context['pk'] = self.kwargs.get('pk')
        return context


class Login(auth_views.LoginView):
    success_url = reverse_lazy('home')
    initial = {
        'username': '',
        'password': '',
    }
    # template_name = 'halls/form.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    initial = {'username': ''}
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        self.form_class.base_fields['password1'].help_text = """Your password can't be too similar to your other personal information.
Your password must contain at least 8 characters.
Your password can't be a commonly used password.
Your password can't be entirely numeric."""

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        uname = form.cleaned_data.get('username')
        passw = form.cleaned_data.get('password1')
        user = authenticate(username=uname, password=passw)
        login(self.request, user)
        return valid

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Sign Up'
        context['submit_btn'] = 'Submit'
        return context
