# forms.py
from django import forms
from django.forms import ModelForm, DateInput
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_when_need': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter patient name...'}),
            'doctor_name': forms.TextInput(attrs={'placeholder': 'Enter doctor name...'}),
            'hospital': forms.Select(attrs={'placeholder': 'Select hospital...'}),
            'blood_group': forms.Select(choices=Patient.BLOOD_GROUPS, attrs={'placeholder': 'Select blood group...'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state...'}),
            'district': forms.TextInput(attrs={'placeholder': 'Enter district...'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter mobile number...'}),
            'other_description': forms.Textarea(attrs={'placeholder': 'Enter other description...'}),
            # Add more widgets as needed
        }

class DonorForm(forms.ModelForm):
    last_donation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    blood_group = forms.ChoiceField(choices=Donor.BLOOD_GROUPS)

    class Meta:
        model = Donor
        fields = '__all__'

class DonationRecordForm(forms.ModelForm):
    class Meta:
        model = DonationRecord
        fields = ['donor', 'donation_date', 'quantity']

    donation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'