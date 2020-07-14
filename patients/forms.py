from django import forms


class PatientForm(forms.Form):
    name = forms.CharField(max_length=150)
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)

