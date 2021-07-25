from farmuser.models import Farm,FarmImage,FarmAvailble,FarmBooking
# from extra_views import CreateWithInlinesView,InlineFormSet
from django import forms


class FarmCreatForm(forms.ModelForm):

    more_image= forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))


    class Meta():
        model = Farm
        fields=('farmname','SizeOfFarm','address','area','city','pincode','image')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['farmname'].label='Farm Name'
        self.fields['SizeOfFarm'].label='Size Of Farm'
        self.fields['image'].label='Display Image'


class DateInput(forms.DateInput):
    input_type = 'date'

class FarmAvailbleForm(forms.ModelForm):
    class Meta:
        model=FarmAvailble
        fields=('farmprice','available')
        widgets = {'available': DateInput(),}

class FarmBookingForm(forms.ModelForm):
    class Meta:
        model=FarmBooking
        fields=('No_of_People',)

