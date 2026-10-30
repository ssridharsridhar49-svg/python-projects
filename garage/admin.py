from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import ContactMessage, CustomDesign, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("company", "name", "category", "image_source")
    list_filter = ("category", "company")
    search_fields = ("company", "name")
    ordering = ("category", "company", "name")

    @admin.display(description="Image source")
    def image_source(self, obj):
        return obj.image_url or (obj.image.name if obj.image else "—")


@admin.register(CustomDesign)
class CustomDesignAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "vehicle", "color", "created_at")
    list_filter = ("vehicle__category", "color", "created_at")
    search_fields = ("name", "user__username", "user__email", "vehicle__name", "vehicle__company")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user", "vehicle")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)


class AutoCraftUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")


admin.site.unregister(User)
admin.site.register(User, AutoCraftUserAdmin)
