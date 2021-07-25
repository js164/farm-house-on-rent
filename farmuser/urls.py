from django.conf.urls import url
from farmuser.models import Farm
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='farmuser'

urlpatterns=[
    url(r'dashboard/$',views.Dashboard.as_view(),name='dashboard'),
    url(r'addfarm/$',views.NewFarm.as_view(),name='addfarm'),
    url(r'available/(?P<pk>\d+)$',views.Available.as_view(),name='available'),
    url(r'farms/$',views.FarmList.as_view(),name='farms'),
    url(r'farms/(?P<pk>\d+)$',views.FarmDetail.as_view(),name='farmdetail'),
    url(r'farmsbookings/$',views.FarmBookings.as_view(),name='farmbookings'),
    url(r'farms/(?P<pk>\d+)/farmupdate$',views.FarmDetailUpdate.as_view(),name='farmupdate'),
    url(r'farms/(?P<pk>\d+)/availableupdate$',views.AvailableUpdate.as_view(),name='availableupdate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
