from blog.models import Post
from django import forms


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'full name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'joe@example.com', 'class': 'form-control'}))
    message = forms.CharField(max_length=150, widget=forms.Textarea(
        attrs={'placeholder': 'leave a message here', 'class': 'form-control'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        return message
