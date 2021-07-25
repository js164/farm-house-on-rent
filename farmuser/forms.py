from betterforms.multiform import MultiModelForm,MultiForm
from farmuser.models import Farm,FarmImage,FarmAvailble,FarmBooking
# from extra_views import CreateWithInlinesView,InlineFormSet
from django import forms


class FarmForm(MultiModelForm):
    form_classes = {
        'farm': Farm,
        'images': FarmImage,
    }

    # def __init__(self,*args,**kwargs):
    #     super(FarmForm,self).__init__(*args,**kwargs)
    #     self.fields['SizeOfFarm'].label='Farm Size(in seq feet)'

# class FarmForm(CreateWithInlinesView):
#     model = Farm
#     inlines = [FarmImage,]

# class FarmImageForm(InlineFormSet):
#     model=FarmImage




class OnlyFarmForm(forms.ModelForm):
    # form_classes = {
    #     'farm': Farm,
    #     'images': FarmImage,
    # }
    # images=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta():
        model = Farm
        fields=('farmname','SizeOfFarm','address','area','city','pincode')
        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

class FarmCreatForm(OnlyFarmForm):

    more_image= forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))


    class Meta(OnlyFarmForm.Meta):
        model = Farm
        fields=('farmname','SizeOfFarm','address','area','city','pincode','image')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['farmname'].label='Farm Name'
        self.fields['SizeOfFarm'].label='Size Of Farm'
        self.fields['image'].label='Display Image'

class FarmImageCreat(forms.ModelForm):
    images=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta():
        model=FarmImage
        fields=('images',)

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

