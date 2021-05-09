from django import forms

from .models import SerachingFarmer,RegisterFarmer,GetDetailsLogin,ForgetPassword,FinalUpdate

class SearchFarmer(forms.ModelForm):
    class Meta:
        model = SerachingFarmer
        fields = ['Town','Quantity','Item','PinCode']

class Registration(forms.ModelForm):
    class Meta:
        model = RegisterFarmer
        fields = ['UserName','Password','ConformPassword','Name','Phone_Number','Item','Organic_Inorganic','City','Quantity','Availability','PinCode']

class GetDetails(forms.ModelForm):
    class Meta:
        model = GetDetailsLogin
        fields = ['GivenUserNum','UserName','Password']

class ChangePassword(forms.ModelForm):
    class Meta:
        model = ForgetPassword
        fields = ['GivenUserNum','Name','City','Password','ConformPassword']

class FinalUpdateDetails(forms.ModelForm):
    class Meta:
        model = FinalUpdate
        fields = ['GivenUserNum','Name','Phone_Number','Item','City','Organic_Inorganic','Quantity','Availability','PinCode']