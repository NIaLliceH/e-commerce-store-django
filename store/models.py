from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True) # short label for category (URL path), require unique
    
    class Meta:
        verbose_name_plural = 'categories' # instead of 'Categorys'
        
    def __str__(self):
        return self.name # display name instead of Category(1), Category(2)
    
    def get_absolute_url(self):
        return reverse("category-result", args=[self.slug])
    
    
    
class Product(models.Model):
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True) # optional field
    slug = models.SlugField(max_length=250) # short label for product, unique if no id field
    price = models.DecimalField(max_digits=8, decimal_places=0) # 99.999.999
    image = models.ImageField(upload_to='images/')
    
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name_plural = 'products'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product-info", args=[self.slug]) # convert to url path