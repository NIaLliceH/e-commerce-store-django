from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma

from .cart import Cart
from store.models import Product


def cart_get(request):
    return render(request, 'cart/cart_view.html')


def cart_add(request):
    cart = Cart(request) # reinit (not Singleton)
    
    data = request.POST # get the request payload
    if data.get('action') == 'post':
        prod_id = str(data.get('product_id'))
        prod_qty = int(data.get('product_quantity'))
        
        # prod = get_object_or_404(Product, id=prod_id)
        cart.add(prod_id, prod_qty)
        
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
    cart = Cart(request)
    
    data = request.POST
    if data.get('action') == 'update':
        prod_id = str(data.get('product_id'))
        prod_qty = int(data.get('product_quantity'))
        cart.update(prod_id, prod_qty)
        
        prod_price = get_object_or_404(Product, id=prod_id).price
        
        response = JsonResponse({
            'message': 'successfully updated product',
            'cart_quantity': cart.__len__(),
            'product_total': intcomma(prod_price * prod_qty),
            'cart_total': intcomma(cart.get_total())
        }, status=200)
        
        return response
    else:
        return JsonResponse({
            'message': 'require update action'
        }, status=400)


def cart_delete(request):
    cart = Cart(request)
    
    data = request.POST
    if data.get('action') == 'delete':
        prod_id = str(data.get('product_id'))
        cart.delete(prod_id)
                
        response = JsonResponse({
            'message': 'succesfully removed from cart',
            # 'product_id': prod_id,
            'cart_quantity': cart.__len__(),
            'cart_total': intcomma(cart.get_total())
        }, status=200)
        
        # session_store = request.session

        # # To view all session data
        # session_data = session_store.items()
        # for key, value in session_data:
        #     print(f"{key}: {value}")
        
        return response
    else:
        return JsonResponse({
            'message': 'require delete action'
        }, status=400)
    
    
    