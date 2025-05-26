from rest_framework import generics, permissions
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, PlasticItemSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import PlasticItem
from .serializers import PlasticItemSerializer
from rest_framework.views import APIView


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
    
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key
        })
    
    
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self,request):
        return Response(status=status.HTTP_200_OK)


class PlasticItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.user.username 
        data = request.data.copy()
        data['username'] = username
        serializer = PlasticItemSerializer(data=data)
        print(data)
        print(serializer.is_valid())
        
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        username = request.user.username 
        if username is not None:
            items = PlasticItem.objects.filter(username=username)
            serializer = PlasticItemSerializer(items, many=True)
            return Response(serializer.data)
        return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)