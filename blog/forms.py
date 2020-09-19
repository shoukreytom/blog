from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'full name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'joe@example.com'}))
    message = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'placeholder': 'leave a message here'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        return message
