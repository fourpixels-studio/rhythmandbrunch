from django.urls import path
from .views import index, contact, gallery

urlpatterns = [
    path("", index, name="index"),
    path("gallery/", gallery, name="gallery"),
    path("contact-us/", contact, name="contact"),

]
