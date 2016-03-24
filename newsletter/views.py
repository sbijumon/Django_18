from django.conf import settings
from django.shortcuts import render
from .forms import SignUpForm, ContactForm
from django.core.mail import send_mail
from .models import SignUp
# Create your views here.


def home(request):
    title = "Sign Up Now"
    #if request.user.is_authenticated():
        #title = "My title"
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        "template_title":title,
        "form":form,
    }
    if request.user.is_authenticated() and request.user.is_staff:
        queryset = SignUp.objects.all().order_by('-timestamp')
        context = {
            "queryset":queryset,
        }
    return render(request, "home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        full_name = form.cleaned_data.get('full_name')
        subject = 'Site Contact Form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s:%s via %s" %(full_name, message, email)
        send_mail(subject,contact_message, from_email,
    to_email, fail_silently=False)

    context = {
        "form":form,
    }
    return render(request, "contact.html", context)


def about(request):
    return render(request, "about.html", {})