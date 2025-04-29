"""
URL configuration for ServireSide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from .views import RegisterView, LoginView, ReceivePublicKeyView, ReceiveHashing, AddFace, Knerast ,SaveHashing



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('receive-public-key/', ReceivePublicKeyView.as_view(), name='receive_public_key'),
    path('receive-hashing/', ReceiveHashing.as_view(), name='receive_hash'),
    path('add-face/', AddFace.as_view(), name='add_face'),
    path('save-hashing/', SaveHashing.as_view(), name='save_hashing'),
    path('knerast/', Knerast.as_view(), name='knerast'),
]
