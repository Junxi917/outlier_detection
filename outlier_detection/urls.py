"""outlier_detection URL Configuration

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
from django.urls import path
from django_web import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'detection'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name='home'),
    path('upload/', v.upload, name='upload'),
    path(r'query', v.query, name='query'),
    path(r'export', v.export, name='export'),
    path(r'export1', v.export1, name='export1'),
    path(r'export2', v.export2, name='export2'),
    path(r'export3', v.export3, name='export3'),
    path(r'export4', v.export4, name='export4'),
    path(r'export5', v.export5, name='export5'),
    path(r'export6', v.export6, name='export6'),

]

urlpatterns += staticfiles_urlpatterns()
