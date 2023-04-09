from django import forms
from gim.models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['speech', 'bpm', 'beats']
        widgets = {
            'speech': forms.TextInput(attrs={'class': 'form-control'}),
            'bpm': forms.TextInput(attrs={'class': 'form-control'}),
            'beats': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'speech': '발언집 이름',
            'bpm': 'BPM',
            'beats': 'Beats'
        }