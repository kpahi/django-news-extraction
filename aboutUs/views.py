from django.shortcuts import render

# Create your views here.
from .forms import ContactForm

def aboutUsIndex(request):
    # add to your views
    form_class = ContactForm

    return render(request, 'AboutUs/aboutUs.html', {
        'form': form_class,
    })
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'AboutUs/aboutUs.html')
