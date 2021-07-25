from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView,RedirectView
from accounts.forms import FarmUserCreateForm,CustUserCreateForm
from accounts.models import FarmUser,CustUser
from django.urls import reverse_lazy,reverse
from django_email_verification import send_email
from django.contrib.auth import authenticate,login
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import random
from django.contrib.auth.models import Group
from decouple import config

# Create your views here.
User=get_user_model()

def OTPVerify(request):
    mobile = request.session['mobile']
    if request.method == 'POST':
        otp = (request.POST.get('otp'))
        user=FarmUser.objects.get(mobile=mobile)

        if otp == str(user.otp):
            print("Sucess")
            send_email(user)
            return redirect('login')
        else:
            print('Wrong')
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/otp.html' , context)
        
    return render(request,'accounts/otp.html')


class FarmSignup(CreateView):
    form_class=FarmUserCreateForm
    template_name='accounts/farmSignup_form.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        group=Group.objects.get(name='FarmOwner')
        user.groups.add(group)
        mobile=form.cleaned_data.get('mobile')
        self.request.session['mobile']=mobile
        otp = str(random.randint(1000 , 9999))
        print(config('SENDOTP'))
        if config('SENDOTP', cast=bool):
            SendOTP(mobile,otp)
        else:
            send_email(user)
        self.object=form.save(commit=False)
        self.object.otp=otp
        self.object.save()
        returnVal = super(FarmSignup, self).form_valid(form)
        return returnVal   

    def get_success_url(self, **kwargs):
        if config('SENDOTP', cast=bool):
            return reverse('accounts:otp')
        else:
            return reverse_lazy('login')

class CustSignup(CreateView):
    form_class=CustUserCreateForm
    template_name='accounts/custuser_form.html'
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        group=Group.objects.get(name='Customer')
        user.groups.add(group)
        return super(CustSignup, self).form_valid(form)  


def SendOTP(mobile,otp):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                body='Please Verify your mobile number! Your OTP is {}'.formate(otp),
                                from_=config('from_mobile'),
                                to='+91{}'.formate(mobile)
                            )
    print("SendOtp called")