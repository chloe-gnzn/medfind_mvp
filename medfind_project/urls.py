from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                          # Django's built-in site (superuser)
    path('', include('landing_app.urls')),                    # landing page (/)
    path('login/', include('login_app.urls')),                      # user login (/login/) + logout
    path('register/', include('register_app.urls')),          # user + pharmacy registration
    path('home/', include('home_app.urls')),                  # user-facing screens
    path('pharmacy-portal/', include('pharmacy_app.urls')),   # pharmacy dashboard
    path('manage/', include('admin_app.urls')),               # MedFind admin panel
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
