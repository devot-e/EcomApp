def global_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart = getattr(request.user, "cart", None)

        if cart:
            cart_count = cart.total_items

    return {
        "cart_count": cart_count,
        "site_name": "EcomApp",
    }