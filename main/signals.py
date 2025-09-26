from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.mail import send_mail
from .models import Tour, Review


# --- Auto-generate slug for Tours ---
@receiver(pre_save, sender=Tour)
def generate_tour_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


# --- Notify admin when a new Review is added ---
@receiver(post_save, sender=Review)
def notify_new_review(sender, instance, created, **kwargs):
    if created:
        subject = f"New Review Submitted by {instance.display_name()}"
        message = f"""
        A new review has been submitted:

        Name: {instance.display_name()}
        Content: {instance.content}
        Date: {instance.created_at.strftime('%b %d, %Y')}
        """
        send_mail(
            subject,
            message,
            "no-reply@mbtravels.com",
            ["info@mbtravels.com"],  # your admin inbox
            fail_silently=True,
        )
