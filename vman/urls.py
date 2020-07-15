"""vman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from importlib.util import find_spec

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from vman import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^{0}$'.format(settings.BASE_URL), TemplateView.as_view(template_name='home.html'), name='home'),
]


namespaces = {getattr(i, 'namespace', None) for i in urlpatterns}
custom_apps = [i.replace('apps.', '') for i in settings.INSTALLED_APPS if i.startswith('apps.')]

for app_name in custom_apps:
    if app_name in namespaces:
        continue

    module_str = 'apps.%s.urls' % app_name
    spec = find_spec(module_str)
    if spec:
        include_urls = include((module_str, app_name))  # namespace=app_name)
        urlpatterns += [url(r'^' + settings.BASE_URL + app_name + '/', include_urls)]
