from django import forms

from .models import SerachingLand,RegisterLand,GetDetailsLogin,ForgetPassword,FinalUpdate

class SearchLand(forms.ModelForm):
    class Meta:
        model = SerachingLand
        fields = ['Town','Acres','PinCode']

class Registration(forms.ModelForm):
    class Meta:
        model = RegisterLand
        fields = ['UserName','Password','ConformPassword','Name','Phone_Number','Acres','R_or_S','City','Rent','Share','Availability','PinCode']

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
        fields = ['GivenUserNum','Name','Phone_Number','Acres','R_or_S','City','Rent','Share','Availability','PinCode']