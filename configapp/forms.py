import re

from django import forms
from django.core.exceptions import ValidationError

from .models import News


class SearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title…'
        })
    )


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        # fields = ['title', 'context', 'is_bool', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'context': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


        def clean_title(self):
            title = self.cleaned_data['title']

            if re.match(r'\d', title):
                print("salom ======================")
                raise ValidationError('Title raqam bo‘lmasin')

            return title