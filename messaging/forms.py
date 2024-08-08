from django import forms 
from .models import Message 
from django_ckeditor_5.widgets import CKEditor5Widget

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'read', 'timestamp']
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='extends', attrs={'class': 'django_ckeditor_5'})
        }
        
        attachments = forms.FileField(widget = forms.TextInput(attrs={
            "name": "attachments",
            "type": "file",
            "class": "form-control",
            "multiple": "true",
        }), label = "")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False