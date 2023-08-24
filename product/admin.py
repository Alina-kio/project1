from django.contrib import admin
from .models import * 


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Application)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Order)
admin.site.register(OrderedItems)