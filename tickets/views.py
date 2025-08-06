from django.shortcuts import render
from events.models import Event


def tickets(request):
    context = {
        "title_tag": "Tickets",
        "latest_event": Event.objects.latest("date"),
    }
    return render(request, "tickets.html", context)
