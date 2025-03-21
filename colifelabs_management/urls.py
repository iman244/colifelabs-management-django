"""
URL configuration for colifelabs_management project.

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
from django.contrib import admin
from django.urls import path, include

from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Colifelabs Adminstration")
admin.site.site_title = _("Colifelabs")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('budgets/', include('budget.urls')),
    path('', admin.site.login),
]
