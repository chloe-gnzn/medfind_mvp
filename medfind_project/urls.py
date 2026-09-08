from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login_app.urls')),      
    path('register/', include('register_app.urls')),  
    path('home/', include('home_app.urls')),        
]
