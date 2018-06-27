"""terkom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static, serve
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [  
#	url('^', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
#    url(r'^login/.*$', auth_views.login,{'template_name': 'myapp/login.html'}, name='login'),
    url(r'^', include('calculation.urls')),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == True:
    #urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar    
    urlpatterns += [
                    url(r'^__debug__/', include(debug_toolbar.urls)),
                    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)