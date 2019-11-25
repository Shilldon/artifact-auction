from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages


def contact(request):
    """
    A view to render a contact form to the page for the user to complete to get
    in contact with the site owner
    """
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid:
            messages.success(request,
                             "Thank you for your enquiry we will be in touch"
                             " within the next 24 hours.")
            email_title = contact_form['subject'].value()
            email_message = contact_form['enquiry'].value() + \
                '\nFrom ' + contact_form['name'].value() + \
                '\n'+contact_form['email_address'].value()
            send_mail(
                email_title,
                email_message,
                contact_form['email_address'].value(),
                ['artifactauction@gmail.com'],
                fail_silently=False, )

            return redirect(reverse('contact'))
    else:
        contact_form = ContactForm()

    return render(request, "contact.html", {"contact_form": contact_form})
