from django.urls import path
from .views import event_detail, event_list, event_schedule

urlpatterns = [
    path("events/", event_list, name="event_list"),
    path("event/<slug:slug>/", event_detail, name="event_detail"),
    path("schedule/event/<slug:slug>/", event_schedule, name="event_schedule"),
]
