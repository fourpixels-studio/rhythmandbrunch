from django.shortcuts import render
from events.models import Event


def index(request):
    events = Event.objects.all()
    latest_event = Event.objects.last()
    context = {
        "events": events,
        "title_tag": "Home",
        "latest_event": latest_event,
    }
    return render(request, "index.html", context)


def contact(request):
    context = {
        "title_tag": "Contact Us",
    }
    return render(request, "contact.html", context)


def gallery(request):
    context = {
        "title_tag": "Gallery",
        "meta_description": "gallery",
    }
    return render(request, "gallery.html", context)
