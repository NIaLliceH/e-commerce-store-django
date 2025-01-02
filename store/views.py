from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def store(request):
    all_prod = Product.objects.all()
    
    data = {'all_products': all_prod}
    
    return render(request, 'store/store.html', context=data)


def categories(request):
    all_cate = Category.objects.all()
    
    return {'all_categories': all_cate}


def category_result(request, cate_slug=None):
    cate = get_object_or_404(Category, slug=cate_slug)
    prods = Product.objects.filter(category=cate)
    data = {
        'category': cate,
        'products': prods
    }
    
    return render(request, 'store/category_result.html', context=data)


def product_info(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    data = {'product': prod}
    
    return render(request, 'store/product_info.html', context=data)