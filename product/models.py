from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save


User = get_user_model()



class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(max_length=255, blank=False)
    image = models.ManyToManyField('ProductImage', related_name='products')

    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    country = models.CharField(max_length=100, blank=True, null=True)
    assembly_required = models.BooleanField(default=False) # требуется сборка или нет

    notes = models.TextField(max_length=500, null=True, blank=True)

    depth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    package_length = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    package_height = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    package_width = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    default_delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, blank=True)
    default_delivery_time = models.IntegerField(default=5, blank=True)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.image.name


class Application(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False, null=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    isOrder = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.product.name)





@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # # cart_items.total_items = len(total_cart_items)

    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()



# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     amount = models.FloatField(default=0)
#     is_paid = models.BooleanField(default=False)
#     order_id = models.CharField(max_length=100, blank=True)
#     payment_id = models.CharField(max_length=100, blank=True)
#     payment_signature = models.CharField(max_length=100, blank=True)


# class OrderedItems(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     order = models.ForeignKey(Orders, on_delete=models.CASCADE)
