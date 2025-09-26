from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.db.models import Q
from .models import Review, Tour
from .forms import ReviewForm


def home(request):
    """
    Home page with latest reviews and AJAX review submission.
    """
    all_reviews = Review.objects.order_by('-created_at')
    latest_reviews = all_reviews[:3]
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            if not review.name:
                review.name = "Anonymous"
            review.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "review": {
                        "id": review.id,
                        "name": review.display_name(),
                        "content": review.content,
                        "created_at": localtime(review.created_at).strftime("%b %d, %Y"),
                    },
                    "is_admin": request.user.is_staff,
                })
            return redirect('home')

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return render(request, "main/home.html", {
        "page_title": "Home",
        "reviews": latest_reviews,
        "form": form,
        "total_reviews": all_reviews.count(),
    })


def about(request):
    return render(request, "main/about.html", {"page_title": "About"})


def contact(request):
    """
    Contact page with optional ?tour= query param to prefill the message box.
    Sends email to admin and confirmation email to user (HTML styled).
    """
    tour_name = request.GET.get("tour", "").strip()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # --- Email to Admin ---
        subject = f"New Safari Inquiry from {name or 'Anonymous'}"
        body = f"""
        Name: {name or 'Anonymous'}
        Email: {email or 'Not provided'}
        Tour: {tour_name if tour_name else 'Not specified'}

        Message:
        {message}
        """

        send_mail(
            subject,
            body,
            email or "no-reply@mbtravels.com",   # from
            ["info@mbtravels.com"],              # to (your inbox)
            fail_silently=False,
        )

        # --- Confirmation Email to User ---
        if email:
            confirm_subject = "We’ve received your safari inquiry"

            html_message = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color:#f9fafb; padding:20px;">
                <div style="max-width:600px; margin:auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                  <div style="background:#facc15; padding:20px; text-align:center;">
                    <h1 style="margin:0; color:#000;">MB Travels</h1>
                  </div>
                  <div style="padding:20px; color:#333;">
                    <p>Hi {name or 'Traveler'},</p>
                    <p>Thanks for reaching out to <strong>MB Travels</strong>! We’ve received your inquiry
                    {f'about the <strong>{tour_name}</strong> safari' if tour_name else ''} and our team will get back to you shortly.</p>
                    
                    <p><strong>Your message:</strong></p>
                    <blockquote style="border-left:4px solid #facc15; margin:10px 0; padding-left:10px; color:#555;">
                      {message}
                    </blockquote>

                    <p>In the meantime, feel free to explore more tours on our website.</p>
                    <p style="margin-top:30px;">Warm regards,<br><strong>MB Travels Team</strong></p>
                  </div>
                  <div style="background:#111; color:#facc15; text-align:center; padding:10px; font-size:12px;">
                    © {localtime().year} MB Travels. All rights reserved.
                  </div>
                </div>
              </body>
            </html>
            """

            plain_message = strip_tags(html_message)

            send_mail(
                confirm_subject,
                plain_message,
                "info@mbtravels.com",  # from
                [email],               # to user
                fail_silently=False,
                html_message=html_message,
            )

        messages.success(request, "Thanks for reaching out! We've sent you a confirmation email.")
        return redirect("contact")

    return render(request, "main/contact.html", {"tour_name": tour_name})


def tours(request):
    """
    Tours page with optional search and featured tours.
    """
    query = request.GET.get('q')
    if query:
        all_tours = Tour.objects.filter(
            Q(location__icontains=query) | Q(name__icontains=query)
        )
    else:
        all_tours = Tour.objects.all()

    featured_tours = Tour.objects.filter(is_featured=True)[:3]

    return render(request, 'main/tours.html', {
        'featured_tours': featured_tours,
        'tours': all_tours
    })


def tour_detail(request, slug):
    """
    Tour detail page using slug instead of pk.
    """
    tour = get_object_or_404(Tour, slug=slug)
    return render(request, 'main/tour_detail.html', {'tour': tour})


@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return JsonResponse({"success": True})


def load_more_reviews(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        reviews = Review.objects.order_by('-created_at')[3:]
        data = [{
            "id": r.id,
            "name": r.display_name(),
            "content": r.content,
            "created_at": localtime(r.created_at).strftime("%b %d, %Y"),
        } for r in reviews]
        return JsonResponse({
            "success": True,
            "reviews": data,
            "is_admin": request.user.is_staff
        })
    return JsonResponse({"success": False}, status=400)


def submit_review(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            return JsonResponse({
                "success": True,
                "review": {
                    "id": review.id,
                    "name": review.display_name(),
                    "content": review.content,
                    "created_at": localtime(review.created_at).strftime("%b %d, %Y"),
                },
                "is_admin": request.user.is_staff,
            })
        return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False})
