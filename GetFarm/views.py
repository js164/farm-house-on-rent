from django.views.generic import TemplateView,RedirectView,CreateView,ListView,DetailView
from django.urls import reverse,reverse_lazy
from django.shortcuts import render
from accounts.models import FarmUser,CustUser
from farmuser.models import Farm,FarmImage,FarmAvailble,FarmBooking
from farmuser.forms import FarmBookingForm
from paytm import checksum
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime

orderId='0'
custId='0'
price='0'

class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {'username': request.user.username }
        try:
            if FarmUser.objects.get(username=request.user.username):
                return redirect('farmuser:dashboard')
            else:
                context = {'farms': Farm.objects.all()[:3:1]}
                return render(request, "dashboard.html", context=context)
        except:
            context = {'farms': Farm.objects.all()[:3:1]}
            return render(request, "dashboard.html", context=context)

class FarmList(ListView):
    model=Farm
    template_name='farm_list.html'

class FindByCity(ListView):
    model=Farm
    template_name="farm_list.html"

    def get_queryset(self):
        queryset=super().get_queryset()
        city=slugify(str(self.kwargs.get('city')))
        if queryset.filter(city=city).count() > 0:
            return queryset.filter(city=city)
        else:
            return super().get_queryset()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        queryset=super().get_queryset()
        context['messages']="Search For City: "+self.kwargs.get("city")
        return context

class FindFarm(ListView):
    model=Farm
    template_name="farm_list.html"

    def get_queryset(self):
        queryset=super().get_queryset()
        farm=self.request.GET.get('farm')
        date=(self.request.GET.get('date'))
        city=self.request.GET.get('city')
        if city:
            queryset= queryset.filter(city=city)
        if date:
            farmavailable=FarmAvailble.objects.filter(available=date).filter(is_booked=False)
            for farm_dates in farmavailable:
                queryset=queryset.filter(id=farm_dates.farm.id)
        if farm:
            farmslug=slugify(str(farm))
            if queryset.filter(slug=farmslug).count() > 0:
                queryset=queryset.filter(slug=farmslug)
        return queryset


class FarmDetail(DetailView):
    model=Farm
    template_name='farm_detail.html'

    def get_context_data(self,*args,**kwargs):
        today = datetime.today().strftime('%Y-%m-%d')
        context=super().get_context_data(**kwargs)
        farm=Farm.objects.get(pk=self.kwargs.get('pk'))
        available=FarmAvailble.objects.filter(farm=farm).filter(available__gte=today)
        farmimages=FarmImage.objects.filter(farm=farm)
        context['farmavailable']=available
        context['farmimages']=farmimages
        return context

class BookingList(LoginRequiredMixin,ListView):
    model=FarmBooking
    template_name='farmbooking_list.html'
    
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user=self.request.user)


class PaymentCheckout(LoginRequiredMixin,CreateView):
    model=FarmBooking
    fields=('No_of_People',)
    template_name='farmbooking_form.html'
    

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.farm=Farm.objects.get(slug=self.kwargs.get('slug1'))
        self.object.farm.is_booked=True
        available=FarmAvailble.objects.get(pk=self.kwargs.get('slug2'))
        self.object.farmavailable=available
        self.object.farm_booking_date=available.available
        self.object.price=available.farmprice
        global orderId,custId,price
        datetoday=datetime.now().strftime('%Y%m%d%H%M%S')
        orderId=datetoday+str(self.object.user.username)+str(available.pk)
        available.booking_order_id=orderId
        available.save()
        self.object.booking_order_id=orderId
        custId=str(self.object.user.email)
        price=str(available.farmprice)
        self.object.save()
        param_dict = {

                'MID': settings.MID_HERE,
                'ORDER_ID': str(orderId),
                'TXN_AMOUNT': price,
                'CUST_ID': custId,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/paymentstatus/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generateSignature(param_dict, settings.M_KEY)
        return render(self.request,'paytm.html',{'param_dict':param_dict})

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        # farm=Farm.objects.get(slug=self.kwargs.get('slug1'))
        farmbooking=FarmAvailble.objects.get(pk=self.kwargs.get('slug2'))
        context['farmbooking']=farmbooking
        return context


   
@csrf_exempt
def paymentstatus(request):
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            paytmchecksum=form[i]
        if i=='ORDERID':
            orderId=form[i]

    verify=checksum.verifySignature(response_dict,settings.M_KEY,paytmchecksum)
    farm=FarmAvailble.objects.get(booking_order_id=orderId)
    if verify:
        if response_dict['RESPCODE']=='01':
            farm.is_booked=True
            farm.save()
            print("Booking Succes")
        else:
            print("Payment Fail"+response_dict['RESPMSG'])
            FarmBooking.objects.get(farmavailable=farm).delete()
    return render(request,'paymentstatus.html',{'response':response_dict})
        


    
