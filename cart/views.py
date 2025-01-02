from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from store.models import Product


def cart_get(request):
    # cart = Cart(request)
    return render(request, 'cart/cart_view.html')


def cart_add(request):
    cart = Cart(request) # reinit (not Singleton)
    
    data = request.POST # get the request payload
    if data.get('action') == 'post':
        prod_id = int(data.get('product_id'))
        prod_qty = int(data.get('product_quantity'))
        
        prod = get_object_or_404(Product, id=prod_id)
        print("ddddd")
        cart.add(prod, prod_qty)
        
        response = JsonResponse({
            'message': 'sucessfully added to cart',
            'cart_quantity': cart.__len__() # total product in cart
        }, status=200)
        return response
    else:
        return JsonResponse({
            'message': 'require post action'
        }, status=400)


def cart_update(request):
    pass


def cart_delete(request):
    pass