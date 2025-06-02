from django import forms
from .models import Feedback


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder':
                                              'Тема отзыва (необязательно)',
                                              'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 5,
                                             'class': 'form-control'}),
        }
