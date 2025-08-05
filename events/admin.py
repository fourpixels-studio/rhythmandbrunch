from django.contrib import admin
from .models import Event, TicketCategory, EventSchedule
admin.site.register(Event)
admin.site.register(TicketCategory)
admin.site.register(EventSchedule)
