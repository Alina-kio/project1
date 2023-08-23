from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

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
    def get(self, request):
        pass

    def post(self, request):
        pass

    def update(self, request):
        pass