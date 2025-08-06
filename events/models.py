from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.templatetags.static import static
from hitcount.models import HitCountMixin, HitCount  # type: ignore
from django.contrib.contenttypes.fields import GenericRelation


class Event(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    poster = models.ImageField(
        upload_to="event_posters/", blank=True, null=True)
    poster_url = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    disclaimer = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    likes = models.CharField(default=0, max_length=9, null=True, blank=True)
    google_maps_link = models.TextField(null=True, blank=True)
    ticket_link = models.TextField(null=True, blank=True)
    meta_thumbnail = ResizedImageField(size=[1200, 630], crop=[
                                       'middle', 'center'], quality=75, upload_to='thumbnails/', blank=True, null=True)
    small_poster = ResizedImageField(
        quality=75, upload_to='thumbnails/', blank=True, null=True)
    online = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="hit_count_generic_relation")

    class Meta:
        ordering = ['-date']

    @property
    def get_share_link(self):
        return f"{settings.MY_SITE}{self.get_url}"

    @property
    def get_ticket_categories(self):
        if TicketCategory.objects.filter(event=self):
            return TicketCategory.objects.filter(event=self)
        return None

    @property
    def get_ticket_price(self):
        if self.get_ticket_categories:
            return round(self.get_ticket_categories[0].price, 0)
        return None

    @property
    def get_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})

    @property
    def view_schedule(self):
        return reverse("event_schedule", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)
        if self.poster and (not self.meta_thumbnail or self.meta_thumbnail.name != f"{self.poster.name}"):
            self.meta_thumbnail.save(
                f"{self.poster.name}", self.poster, save=False)
            super(Event, self).save(update_fields=['meta_thumbnail'])
        if self.poster and (not self.small_poster or self.small_poster.name != f"{self.poster.name}"):
            self.small_poster.save(
                f"{self.poster.name}", self.poster, save=False)
            super(Event, self).save(update_fields=['small_poster'])

    @property
    def get_meta_thumbnail(self):
        if self.meta_thumbnail:
            return self.meta_thumbnail.url
        return static('rhythymandbrunch_meta_thumbnail.jpg')

    @property
    def get_small_poster(self):
        if self.small_poster:
            return self.small_poster.url
        return static('rhythymandbrunch_small_poster.jpg')

    @property
    def get_poster(self):
        if self.poster:
            return self.poster.url
        if self.poster_url:
            return self.poster_url
        return static('rhythymandbrunch_poster.jpg')

    @property
    def is_upcoming(self):
        if self.date >= timezone.now().date():
            return "Upcoming"
        return "Past"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-date']

    @property
    def get_hit_count(self):
        if self.hit_count_generic.exists():
            return self.hit_count_generic.first().hits
        return 0

    @property
    def get_schedule(self):
        if EventSchedule.objects.filter(event=self).exists():
            return EventSchedule.objects.filter(event=self)
        return None

    @property
    def get_tickets(self):
        if TicketCategory.objects.filter(event=self).exists():
            return TicketCategory.objects.filter(event=self)
        return None


class TicketCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, blank=True, unique=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    admits = models.IntegerField(default=1)
    sold_out = models.BooleanField(default=False)
    ticket_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category_name} - {self.event.name}"


class EventSchedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    performer = models.TextField(blank=True, null=True)
    performance_description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(
        upload_to="schedule_images/", blank=True, null=True)
    thumbnail = ResizedImageField(
        quality=75, upload_to='thumbnails/', blank=True, null=True)
    size_small = ResizedImageField(
        size=[876, 876], quality=75, upload_to='thumbnails/', blank=True, null=True)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['start_time']

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return static('performer_placeholder.jpg')

        return

    def __str__(self):
        return f"{self.performer} - {self.event.name}"
