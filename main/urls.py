from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Tours
    path("tours/", views.tours, name="tours"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour_detail"),  # ✅ now uses slug

    # Reviews
    path("reviews/submit/", views.submit_review, name="submit_review"),
    path("reviews/load-more/", views.load_more_reviews, name="load_more_reviews"),
    path("delete-review/<int:review_id>/", views.delete_review, name="delete_review"),

    # CKEditor
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
