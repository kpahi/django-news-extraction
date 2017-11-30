from django import forms

# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(label='Your name', max_length=100, required=True)
    contact_email = forms.EmailField(label='Your email', max_length=100, required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
