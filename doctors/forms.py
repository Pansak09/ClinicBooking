from django import forms
from .models import Doctor, DoctorCheckin

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'contact', 'address', 'image']

class DoctorCheckinForm(forms.ModelForm):
    checkin_at = forms.DateTimeField(
        label="วันที่เข้าทำงาน",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = DoctorCheckin
        fields = ['checkin_at', 'note']
