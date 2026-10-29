from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Product, Review


def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    return render(
        request,
        "product/product_list.html",
        {"products": products},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related("user")
    average_rating = reviews.aggregate(avg=Avg("rating"))["avg"]

    return render(
        request,
        "product/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "average_rating": average_rating,
        },
    )


@login_required
@require_POST
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    rating = request.POST.get("rating", "")
    comment = request.POST.get("comment", "").strip()

    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Choose a rating from 1 to 5.")
        return redirect("product:product_detail", pk=pk)

    Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={"rating": rating, "comment": comment},
    )

    messages.success(request, "Your review has been saved.")
    return redirect("product:product_detail", pk=pk)