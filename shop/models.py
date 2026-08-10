from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    price = models.DecimalField("price", decimal_places=2, max_digits=10)
    
    slug = models.SlugField("slug", unique=True)
    
    created_at = models.DateTimeField("created", auto_now_add=True)

    modified_at = models.DateTimeField("modified", auto_now=True)
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images") 
    
    image = models.ImageField("images", upload_to="products/")
    
       