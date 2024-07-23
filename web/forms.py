from django.contrib.auth.forms import UserCreationForm
from django import forms

from people_queue.models import QueueMember


class MembersCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя',
        'class': 'form-control py-3'
    }))
    class Meta:
        model = QueueMember
        fields = ('name',)