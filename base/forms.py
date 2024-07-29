from django import forms
from base.models import EmpInfo

class EmpForm(forms.ModelForm):
    class Meta:
        model=EmpInfo
        exclude = ['dept']
        # fields="__all__"

# class AttForm(forms.ModelForm):
#     class Meta:
#         model=Attendance
#         fields="__all__"

class MyForm(forms.Form):
    eid=forms.CharField(label="Employee Id",max_length=30,widget=forms.TextInput(attrs={ 'style': 'width: 200px; padding: 5px; margin:10px;'}) )
    password=forms.CharField(label="Password",max_length=20,widget=forms.PasswordInput(attrs={ 'style': 'width: 200px;padding: 5px; margin:10px;margin-left:20px;'}))

class Search(forms.Form):
    search=forms.CharField(label="Employee Id",max_length=30 )
    month=forms.CharField(label="Month",widget=forms.TextInput(attrs={'placeholder': 'Jan, Feb...'}))
    year=forms.CharField(label="Year")

class empSearch(forms.Form):
    month=forms.CharField(label="Month",widget=forms.TextInput(attrs={'placeholder': 'Jan, Feb...'}))
    year=forms.CharField(label="Year")

class SearchEmpinfo(forms.Form):
    eid=forms.CharField(label="Employee ID",max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Search'}) )

class Email(forms.Form):
    email=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Write your Message...'}), max_length=300)
    
class EmailAdmin(forms.Form):
    rec=forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'To'}), max_length=300)
    email=forms.CharField(label='',widget=forms.Textarea(attrs={"rows":8, "cols":20,'placeholder':'Write your message','style': 'padding: 2px;'}))
    