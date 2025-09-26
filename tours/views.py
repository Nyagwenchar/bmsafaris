# tours/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
import logging

from .models import Tour
try:
    from .forms import BookingForm
except Exception:
    BookingForm = None
    logging.warning("BookingForm could not be imported; booking forms will be disabled.")

def tour_list(request):
    tours = Tour.objects.filter(featured=True)
    return render(request, 'tours/list.html', {'tours': tours})

def tour_detail(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    return render(request, 'tours/detail.html', {'tour': tour})

def tour_book(request, slug):
    tour = get_object_or_404(Tour, slug=slug)

    if request.method == 'POST' and BookingForm is not None:
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail(
                    f"Booking Confirmation: {tour.name}",
                    f"Hi {data.get('full_name','')}, thanks for booking {tour.name} for {data.get('attendees','')} guest(s).",
                    'no-reply@bmsafaris.com',
                    [data.get('email')],
                )
            except Exception:
                logging.exception("Failed to send booking confirmation email")
                messages.error(request, "Booking received but confirmation email failed to send.")
            else:
                messages.success(request, "Booking received. A confirmation email has been sent.")
            return render(request, 'tours/booking_success.html', {'tour': tour})
    else:
        form = BookingForm() if BookingForm is not None else None

    return render(request, 'tours/book.html', {
        'tour': tour,
        'form': form,
    })
