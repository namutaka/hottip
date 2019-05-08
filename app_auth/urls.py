from django.urls import path, re_path, include
from django.contrib.auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('social/', include('social_django.urls', namespace='social')),
]
