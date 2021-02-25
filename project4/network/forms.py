from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':  'Enter your post',
                             'rows': '3', 'class': 'form-control'}), label='')
    class Meta:
        model = Posts
        fields = ['body',]
