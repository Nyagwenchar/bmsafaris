# tours/admin.py
from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display        = ("name", "region", "duration", "price", "featured")
    list_filter         = ("region", "featured")
