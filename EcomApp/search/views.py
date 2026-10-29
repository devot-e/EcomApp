from django.db.models import Q
from django.shortcuts import render

from product.models import Product


def search_products(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
        ).order_by("name")

    return render(
        request,
        "search/search_results.html",
        {
            "query": query,
            "products": products,
        },
    )