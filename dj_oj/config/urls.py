"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import private_storage.urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('problems/', include('problems.urls')),
    path('submissions/', include('submissions.urls')),
    path('api/submissions/', include('submissions.api.urls')),
]

urlpatterns += [
    path('private-media/', include(private_storage.urls)),
    path('tinymce/', include('tinymce.urls')),
]
