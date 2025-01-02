from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:prod_slug>', views.product_info, name='product-info'), # pass slug as a param
    path('category/<slug:cate_slug>', views.category_result, name='category-result')
]
