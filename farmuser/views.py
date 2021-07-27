from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,DetailView,TemplateView,UpdateView
from farmuser.forms import FarmCreatForm,FarmAvailbleForm
from django.urls import reverse_lazy,reverse
from farmuser.models import Farm,FarmImage,FarmAvailble,FarmBooking
from accounts.models import FarmUser,CustUser
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import get_object_or_404

User=get_user_model()
# Create your views here.

class Dashboard(TemplateView):
    template_name='farmuser/dashboard.html'

    def get_context_data(self,**kwargs):
        today = datetime.today().strftime('%Y-%m-%d')
        totalfarms=Farm.objects.filter(user=self.request.user).count()
        upcomingfarmbookings=FarmBooking.objects.filter(farm__in=Farm.objects.filter(user=self.request.user)).filter(farm_booking_date__gte=today).count()
        context={'totalfarms':totalfarms,'upcomingbookings':upcomingfarmbookings}
        return context

class NewFarm(CreateView):
    form_class=FarmCreatForm
    template_name='farmuser/addfarm_form.html'
    # success_url=reverse_lazy('dashboard')

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        images = self.request.FILES.getlist("more_image")
        for i in images:
            FarmImage.objects.create(farm=self.object, image=i)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('farmuser:farmdetail',kwargs={'pk':self.object.id})

class FarmList(ListView):
    model=Farm

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user=self.request.user)

        

class FarmDetail(DetailView):
    model=Farm

    def get_context_data(self,*args,**kwargs):
        today = datetime.today().strftime('%Y-%m-%d')
        context=super().get_context_data(**kwargs)
        farm=Farm.objects.get(pk=self.kwargs.get('pk'))
        available=FarmAvailble.objects.filter(farm=farm).filter(available__gte=today)
        farmimages=FarmImage.objects.filter(farm=farm)
        context['farmavailable']=available
        context['farmimages']=farmimages
        return context

class Available(CreateView):
    form_class=FarmAvailbleForm
    template_name='farmuser/farmavailble_form.html'

    def form_valid(self,form):
        self.object=form.save(commit=False)
        farmslug=str(self.kwargs.get('slug'))
        self.object.farm=Farm.objects.get(pk=self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('farmuser:farmdetail',kwargs={'pk':self.kwargs['pk']})

class FarmBookings(ListView):
    model=FarmBooking

    def get_queryset(self):
        farmbooking=FarmBooking.objects.filter(farm__in=Farm.objects.filter(user=self.request.user))
        return farmbooking


class FarmDetailUpdate(UpdateView,LoginRequiredMixin):
    login_url='/login/'
    form_class=FarmCreatForm
    model=Farm
    template_name='farmuser/addfarm_form.html'

    def get_success_url(self):
        return reverse('farmuser:farmdetail',kwargs={'pk':self.kwargs.get('pk')})

class AvailableUpdate(UpdateView,LoginRequiredMixin):
    login_url='/login/'
    form_class=FarmAvailbleForm
    model=FarmAvailble
    template_name='farmuser/farmavailble_form.html'

    def get_success_url(self):
        farm=Farm.objects.get(farmname=FarmAvailble.objects.get(pk=self.kwargs.get('pk')).farm)
        return reverse('farmuser:farmdetail',kwargs={'pk':farm.pk})