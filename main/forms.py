from django import forms
from .models import RequirementBlock




class RBForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RBForm, self).__init__(*args, **kwargs)
        self.fields['value'].label = False

    class Meta:
        model = RequirementBlock
        exclude = ('id', 'requirement')
