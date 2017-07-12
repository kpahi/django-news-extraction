from django import forms


class NewsFilterForm(forms.Form):
    # body = models.CharField(max_length=255, blank=True, null=True)
    your_name = forms.CharField(label='Your name', max_length=100)
    dateStart = forms.DateField()
    dateEnd = forms.DateField()
    dateRangePicker = forms.CharField(max_length=50)
