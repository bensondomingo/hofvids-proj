from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import HallForm, VideoForm


def home(request):
    return render(request, 'halls/home.html')


def dashboard(request):
    return render(request, 'halls/dashboard.html')


def add_video(request, pk):
    if request.method == 'GET':
        form = VideoForm()
        return render(request, 'halls/addvideo.html', {'form': form})

    # fields = ['title', 'url', 'youtube_id']
    form = VideoForm(request.POST)
    if form.is_valid():
        video = Video()
        video.title = form.cleaned_data['title']
        video.url = form.cleaned_data['url']
        video.youtube_id = form.cleaned_data['youtube_id']
        video.hall = Hall.objects.get(pk=pk)
        video.save()
        return redirect(reverse_lazy('detailhall', kwargs={'pk': pk}))


class AddVideo(generic.CreateView):
    form_class = VideoForm
    initial = {
        'title': '',
        'url': '',
        'youtube_id': '',
    }
    template_name = 'halls/addvideo.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            video = Video()
            video.title = form.cleaned_data['title']
            video.url = form.cleaned_data['url']
            video.youtube_id = form.cleaned_data['youtube_id']
            video.hall = Hall.objects.get(pk=kwargs.get('pk'))
            video.save()
            return redirect(reverse_lazy('detailhall', kwargs=kwargs))


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
