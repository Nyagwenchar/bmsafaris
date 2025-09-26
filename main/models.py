from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse


class Review(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def display_name(self):
        return self.name if self.name else "Anonymous"

    def __str__(self):
        return f"{self.display_name()} - {self.content[:30]}"


class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # ✅ added for SEO-friendly URLs
    location = models.CharField(max_length=200)
    description = models.TextField()
    detailed_info = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to="tours/", blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # ✅ numeric
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug if missing
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"slug": self.slug})


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="tours/gallery/")
    caption = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Tour Image"
        verbose_name_plural = "Tour Images"

    def __str__(self):
        return f"{self.tour.name} - {self.caption or 'Extra Image'}"
