from django.db import models
from django.utils.timezone import now
from django.utils.timesince import timesince


class Contact(models.Model):
    first_name = models.CharField(max_length=180, blank=True, null=True)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name

    @property
    def get_notification(self):
        name = self.first_name[:40] if self.first_name[:40] else "John Doe"
        time_since = timesince(self.date, now()).split(",")[
            0] if self.date else "just now"
        return f"{name} sent a message {time_since} ago saying {self.message[:30]}"
