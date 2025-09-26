from django.contrib import admin
from django.utils.html import format_html
from .models import Review, Tour, TourImage


# --- Review Admin ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'content', 'created_at')
    search_fields = ('id', 'name', 'content')
    ordering = ('-created_at',)


# --- Inline for Tour Images ---
class TourImageInline(admin.TabularInline):  # use StackedInline if you prefer larger previews
    model = TourImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius:4px;" />', obj.image.url)
        return format_html('<span style="color: #999;">No Image</span>')
    image_preview.short_description = "Preview"


# --- Tour Admin ---
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'duration', 'price', 'is_featured', 'image_preview')
    list_display_links = ('name',)
    list_editable = ('is_featured',)
    search_fields = ('name', 'location')
    list_filter = ('is_featured', 'location')
    readonly_fields = ('image_preview',)
    inlines = [TourImageInline]
    ordering = ('-id',)

    # --- Bulk Actions ---
    actions = ["mark_as_featured", "mark_as_unfeatured"]

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} tour(s) successfully marked as Featured ✅")
    mark_as_featured.short_description = "Mark selected tours as Featured"

    def mark_as_unfeatured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} tour(s) successfully unmarked as Featured ❌")
    mark_as_unfeatured.short_description = "Unmark selected tours as Featured"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius:4px;" />', obj.image.url)
        return format_html('<img src="/static/images/placeholder-tour.jpg" style="width: 100px; height: auto; border-radius:4px;" />')
    image_preview.short_description = "Main Preview"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
