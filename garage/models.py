from django.conf import settings
from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    CATEGORY = [
        ("car", "Car"),
        ("bike", "Bike"),
    ]

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY)
    # FileField avoids requiring Pillow at startup. Catalog vehicles can use an
    # uploaded local image or an image_url for the existing hosted catalogue.
    image = models.FileField(upload_to="vehicles/", blank=True)
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ("company", "name")

    def __str__(self):
        return f"{self.company} {self.name}"

    @property
    def display_image(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ""


class CustomDesign(models.Model):
    COLOR_CHOICES = [
        ("#f4f4f4", "Arctic white"),
        ("#171717", "Midnight black"),
        ("#d92d20", "Racing red"),
        ("#175cd3", "Track blue"),
        ("#12b76a", "Emerald green"),
        ("#d0a14b", "Brushed bronze"),
    ]
    WHEEL_CHOICES = [
        ("stock", "Factory finish"),
        ("street", "Street alloy"),
        ("track", "Forged track"),
        ("offroad", "All-terrain"),
    ]
    SPOILER_CHOICES = [
        ("none", "No spoiler / stock tail"),
        ("sport", "Sport spoiler / tail tidy"),
        ("gt", "GT wing / race cowl"),
        ("touring", "Touring setup"),
    ]
    STICKER_CHOICES = [
        ("none", "No graphics"),
        ("stripes", "Racing stripes"),
        ("number", "Race number"),
        ("decals", "Custom decals"),
    ]
    EXHAUST_CHOICES = [
        ("stock", "Factory exhaust"),
        ("sport", "Sport exhaust"),
        ("performance", "Performance system"),
        ("titanium", "Titanium finish"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="custom_designs",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="custom_designs",
    )
    name = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="#171717")
    wheels = models.CharField(max_length=30, choices=WHEEL_CHOICES, default="stock")
    spoiler = models.CharField(max_length=30, choices=SPOILER_CHOICES, default="none")
    stickers = models.CharField(max_length=30, choices=STICKER_CHOICES, default="none")
    exhaust = models.CharField(max_length=30, choices=EXHAUST_CHOICES, default="stock")
    accessories = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} — {self.vehicle} ({self.name or 'Custom design'})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"
