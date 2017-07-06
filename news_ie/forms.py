from django import forms


class NameForm(forms.Form):
    #news = forms.CharField(label='detail news', max_length=500)
    news_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
