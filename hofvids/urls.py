"""hofvids URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from halls import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    # AUTH
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Halls
    # path('halloffame/create/', views.create_hall, name='create_hall'),
    path('halloffame/create/', views.CreateHall.as_view(), name='createhall'),
    path('hof/create/', views.create_hall, name='create_hall'),
    path('halloffame/<int:pk>/', views.DetailHall.as_view(), name='detailhall'),
    path('halloffame/<int:pk>/update/', views.UpdateHall.as_view(), name='updatehall'),
    path('halloffame/<int:pk>/delete/', views.DeleteHall.as_view(), name='deletehall'),
    # Videos
    # path('halloffame/<int:pk>/addvideo/', views.add_video, name='addvideo'),
    path('halloffame/<int:pk>/addvideo/', views.AddVideo.as_view(), name='addvideo'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)