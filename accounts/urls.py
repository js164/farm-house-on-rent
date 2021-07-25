from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from django_email_verification import urls as email_urls

app_name='accounts'

urlpatterns=[
    url(r'login/$',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    url(r'logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'farmsignup/$',views.FarmSignup.as_view(),name='farmsignup'),
    url(r'signup/$',views.CustSignup.as_view(),name='custsignup'),
    url(r'mobileverify/',views.SendOTP,name='sendotp'),
    path('email/', include(email_urls)),
    path('otp/',views.OTPVerify,name='otp'),
]       