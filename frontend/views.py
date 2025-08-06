from .forms import ContactForm
from events.models import Event
from django.contrib import messages
from django.shortcuts import render, redirect


def index(request):
    events = Event.objects.all()
    latest_event = Event.objects.latest("date")
    context = {
        "events": events,
        "title_tag": "Home",
        "latest_event": latest_event,
    }
    return render(request, "index.html", context)


def contact(request):
    latest_event = Event.objects.latest("date")
    contact_form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            # send_confirmation_message_email() TO DO
            return render(request, "contact.html", {"success": True})
        else:
            if contact_form.errors:
                for field, errors in contact_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    context = {
        "title_tag": "Contact Us",
        "latest_event": latest_event,
        "contact_form": contact_form,
    }
    return render(request, "contact.html", context)


def gallery(request):
    context = {
        "title_tag": "Gallery",
        "meta_description": "gallery",
    }
    return render(request, "gallery.html", context)
