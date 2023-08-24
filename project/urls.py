from django.contrib import admin
from django.urls import path
from product import views
from . import swagger
from django.conf import settings
from django.conf.urls.static import static
from product.views import *
from product import views
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [

    path('admin/', admin.site.urls),

    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    # path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('category/', views.CategoryAPIViewSet.as_view(
        {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),

    path('product/', views.ProductsAPIView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('product/<int:pk>/', views.ProductsDetailAPIViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('application/', app),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', order),
    path('orderitems/', OrderItemsAPI.as_view(), name='orderitems'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += swagger.urlpatterns