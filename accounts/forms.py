from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import FarmUser,CustUser

class FarmUserCreateForm(UserCreationForm):

    class Meta:
        fields=('username','email','password1','password2','mobile')
        model=FarmUser

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Display Name'
        self.fields['email'].label='Email Address'

class CustUserCreateForm(UserCreationForm):

    class Meta:
        fields=('username','email','mobile','password1','password2')
        model=CustUser

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Display Name'
        self.fields['email'].label='Email Address'
