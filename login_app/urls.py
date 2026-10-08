from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),          # general users
    path('logout/', views.logout_view, name='logout'),
]
