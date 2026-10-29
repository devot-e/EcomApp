from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("<int:pk>/review/", views.add_review, name="add_review"),
]