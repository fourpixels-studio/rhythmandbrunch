from .models import Event
from django.shortcuts import render


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    context = {
        "event": event,
        "title_tag": f"{event.name} Event",
    }
    return render(request, "event_detail.html", context)


def event_list(request):
    context = {
        "title_tag": "Events",
        "events": Event.objects.all(),
    }
    return render(request, "event_list.html", context)


def event_schedule(request, slug):
    event = Event.objects.get(slug=slug)
    context = {
        "event": event,
        "title_tag": f"{event.name} Schedule",
        "meta_description": f"schedule for {event.name}",
    }
    return render(request, "schedule.html", context)
