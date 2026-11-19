
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from product.models import Product


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related("product").all()

    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
            "items": items,
            "total": cart.total_price,
        },
    )


@login_required
@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.stock <= 0:
        messages.error(request, "Product is out of stock.")
        return redirect("product:product_detail", pk=pk)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(quantity, 99))

    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock or new_quantity > 99:
                messages.error(request, "Not enough stock available.")
                return redirect("product:product_detail", pk=pk)

            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity", "updated_at"])

    messages.success(request, "Product added to your cart.")
    return redirect("cart:cart_detail")


@login_required
@require_POST
def update_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=pk,
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Product removed from cart.")

    elif quantity > cart_item.product.stock or quantity > 99:
        messages.error(request, "Requested quantity is unavailable.")

    else:
        cart_item.quantity = quantity
        cart_item.save(update_fields=["quantity", "updated_at"])
        messages.success(request, "Cart updated successfully.")

    return redirect("cart:cart_detail")


@login_required
@require_POST
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)

    CartItem.objects.filter(
        cart=cart,
        product_id=pk,
    ).delete()

    messages.success(request, "Product removed from cart.")
    return redirect("cart:cart_detail")
