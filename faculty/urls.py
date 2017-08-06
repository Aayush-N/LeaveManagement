"""faculty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView

from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from leaves.views import LoginForm1

from leaves.views import (
	home_view,
	apply_view,
	my_leave_view,
	exhausted_view,
	approval_view,
	help_view,
	account_view,
)

admin.site.site_header = 'FLM Administration'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm1}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^$', home_view),
    #url(r'^home/$', home_view),
    url(r'^apply/$', apply_view),
    url(r'^my-leaves/$', my_leave_view),
    url(r'^history/$', home_view),
    url(r'^approve/$', home_view),
    url(r'^exhausted/$', exhausted_view),
    url(r'^account/$', account_view),
    url(r'^help/$', help_view),
    url(r'^approvals/(?P<name>[^/]+)/(?P<cat>[^/]+)/(?P<fromd>[^/]+)/(?P<endd>[^/]+)/(?P<days>[0-9]+)/$', approval_view),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^(?!/?static/)(?P<path>.*\..*)$', RedirectView.as_view(url='/static/%(path)s', permanent=False)),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
