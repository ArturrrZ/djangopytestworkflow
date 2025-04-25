from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home),
    path('users/', views.users),
    path('accounts/', include('django.contrib.auth.urls')),
    path('secured/', views.secured)
]
