"""GetFarm URL Configuration

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
from django.urls import path,include,re_path
from django.conf.urls import url
from . import views
from django_email_verification import urls as email_urls
from django.conf import settings
from django.conf.urls.static import static,serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include(('accounts.urls','accounts'),namespace='accounts')),
    path('',views.Dashboard.as_view(),name='dashboard'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('email/', include(email_urls)),
    path('farmuser/',include(('farmuser.urls','farmuser'),namespace='farmuser')),
    url(r'bookfarm/(?P<slug1>[-\w]+)/(?P<slug2>[-\w]+)/$',views.PaymentCheckout.as_view(),name='paymentcheckout'),
    path('paymentstatus/',views.paymentstatus,name='paymentstatus'),
    path('farms/',views.FarmList.as_view(),name='farms'),
    url(r'farms/(?P<pk>\d+)$',views.FarmDetail.as_view(),name='farmdetail'),
    path('mybookings/',views.BookingList.as_view(),name='showbookings'),
    path('findfarm/',views.FindFarm.as_view(),name='findfarm'),
    path('findbycity/<str:city>/',views.FindByCity.as_view(),name='findbycity'),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)