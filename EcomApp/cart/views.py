from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from product.models import Product


def cart_detail(request):
    cart = request.session.get("cart", {})
    product_ids = [int(pk) for pk in cart.keys()]

    products = Product.objects.filter(pk__in=product_ids)
    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = int(cart.get(str(product.pk), 0))
        if quantity <= 0:
            continue

        subtotal = product.price * quantity
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })
        total += subtotal

    return render(
        request,
        "cart/cart_detail.html",
        {"items": items, "total": total},
    )


@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get("cart", {})
    key = str(product.pk)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(quantity, 99))
    current_quantity = int(cart.get(key, 0))
    new_quantity = current_quantity + quantity

    if product.stock < new_quantity:
        messages.error(request, "Not enough stock available.")
        return redirect("product:product_detail", pk=pk)

    cart[key] = new_quantity
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, "Product added to your cart.")
    return redirect("cart:cart_detail")


@require_POST
def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get("cart", {})
    key = str(product.pk)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart.pop(key, None)
    elif quantity > product.stock or quantity > 99:
        messages.error(request, "Requested quantity is unavailable.")
    else:
        cart[key] = quantity

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart:cart_detail")


@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart:cart_detail")