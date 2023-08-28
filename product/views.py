from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

class CategoryAPIViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partual_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


from rest_framework.decorators import api_view
    

class ProductsAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partual_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]



class ProductsDetailAPIViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partual_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]





class ApplicationView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def telegram_bot_sendtext(bot_message):
        bot_token = '6655455611:AAHyLQ5kngfETC6hqIRfnxubm7vpX6u-Yeg'
        bot_chatID = '715766595'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
    


@api_view(['POST'])
@permission_classes([AllowAny])
def app(request):
    print(request.user)
    if request.method == 'GET':
        application = Application.objects.all()
        data = ApplicationSerializer(application, many=True).data
        return Response(data=data)
    if request.method == 'POST':
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Сохраняем заявку в базу данных
            new_application = serializer.instance   # Получаем объект только что созданной заявки
            message = f"New message\n\nName: {new_application.name}\nPhone: {new_application.phone_number}\nText: {new_application.text}"
            test = ApplicationView.telegram_bot_sendtext(message)
            print(test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)
        # return Response({'success': 'permissions working'})

    def post(self, request):
        data = request.data
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, ordered=False)
        
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        total_price = 0
        cart_items = CartItems.objects.filter(user=user, cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()

        return Response({'success': 'Items Added to your cart.'})


    def put(self, request):
        data = request.data
        cart_items = CartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_items.quantity += quantity
        cart_items.save()



        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, ordered=False)
        total_price = 0
        cart_items = CartItems.objects.filter(user=user, cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Updated.'})



    def delete(self, request):
        user = request.user
        data = request.data

        cart_items = CartItems.objects.get(id=data.get('id'))
        cart_items.delete()

        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)
    


class OrderItemsView(ModelViewSet):
    # def get(self, request):
    #     queryset = OrderedItems.objects.filter(user = request.user)
    #     serializer = OrderItemsSerializer(queryset, many=True)
    #     return Response(serializer.data)
    queryset = OrderedItems.objects.all()
    serializer_class = OrderItemsSerializer




class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def telegram_bot_sendtext(bot_message):
        bot_token = '6530814720:AAFw81Gh18RQtbh2qNeRdijNGZsOLnxAhng'
        bot_chatID = '715766595'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order(request):
    # print(request.user)
    if request.method == 'GET':
        queryset = Order.objects.filter(user = request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        if not cart:
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        order = Order.objects.create(
            user=user,
            name=request.data.get('name'),
            cart=cart,
            total_price=cart,
            address=request.data.get('address'),
            phone_number=request.data.get('phone_number')
        )

        cart_items = CartItems.objects.filter(cart=cart)

        order_summary = (
            f"Имя: {order.name}\n"
            f"Адрес: {order.address}\n"
            f"Номер телефона: {order.phone_number}\n\n"
            f"Товары:\n"
        )
        
        for cart_item in cart_items:
            item_summary = (
                f"Продукт: {cart_item.product.name}\n"
                f"количество: {cart_item.quantity}\n"
                f"Цена: {cart_item.price}\n\n"
            )
            order_summary += item_summary

        order_summary += f"\nобщая цена: {order.total_price}"

        print(order_summary)
        test = OrderView.telegram_bot_sendtext(order_summary)
        print(test)

        return Response({'success': 'Order created and details printed.'})