from django import forms
from .models import Thesis, Approval

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['title', 'description', 'file']

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ['is_approved']
