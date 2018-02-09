# forms.py
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from .models import Form


class ButtonWidget(forms.Widget):
    template_name = 'auth_button_widget.html'

    def render(self, name, value, attrs=None):
        context = {
            'url': '/'
        }
        return mark_safe(render_to_string(self.template_name, context))


class FormForm(forms.ModelForm):
    #button = forms.CharField(widget=ButtonWidget)
    def clean(self):
        cleaned_data = self.cleaned_data
        batchFile = cleaned_data.get('batchFile')
        if  batchFile is not None:
           tmp = str(batchFile).lower()
           if not tmp.endswith('.zip'):
            raise forms.ValidationError(u"必须上传zip格式")
        return cleaned_data
    class Meta:
        model = Form
        fields = "__all__"
