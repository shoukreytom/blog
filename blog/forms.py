from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'full name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'joe@example.com'}))
    message = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'placeholder': 'leave a message here'}))
