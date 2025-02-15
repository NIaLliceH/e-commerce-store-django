from copy import deepcopy

from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session # copy by reference -> require this to update later
        
        if 'cart_info' not in self.session:
            self.session['cart_info'] = {} # new customer -> create cart_info
        
        self.data = self.session['cart_info'] # cart_info keep cart cache (prod_id: price, qty)
    
    
    def add(self, product_id: str, product_quantity: int):
        # product_id = str(product.id)
        
        if product_id in self.data:
            self.data[product_id]['qty'] += product_quantity # add this prod_id with qty into cart
        else:
            self.data[product_id] = {
                # 'price': str(product.price), # should not store price since it might change
                'qty': product_quantity
            }

        self.session.modified = True # notify session has been modified
    
    
    def update(self, product_id: str, product_quantity: int):
        if product_id in self.data:
            self.data[product_id]['qty'] = product_quantity
            
            self.session.modified = True
        
        
    def delete(self, product_id: str):        
        if product_id in self.data:
            del self.data[product_id]
            
            self.session.modified = True
        
        
    def get_total(self):
        return sum(item['product'].price * item['qty'] for item in self.__iter__())
    
    
    def __len__(self):
        return sum(item['qty'] for item in self.data.values())
        
        
    def __iter__(self): # for item in Cart obj
        # cart = self.data.copy() # shallow copy
        cart = deepcopy(self.data)
            
        for prod_id in cart.keys():
            prod = Product.objects.get(id=prod_id)
            cart[prod_id]['product'] = prod
            yield cart[prod_id]