"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import login
from django.urls import path
from django.conf.urls import include
from django.utils import translation
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from serverapi.views import Comments, Voices, Birdies, Categories, login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', Comments, 'comment')
router.register(r'voices', Voices, 'voice')
router.register(r'birdies', Birdies, 'birdie')
router.register(r'categories', Categories, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
