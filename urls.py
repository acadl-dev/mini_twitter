# mini_twitter/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/accounts/', include('accounts.urls')),  # Inclua as URLs de 'accounts'
    path('api/posts/', include('posts.urls')),  # Inclua as URLs do módulo 'posts' aqui      
    path('api/users/', include('users.urls')),  # Inclua as URLs do módulo 'posts' aqui      
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
