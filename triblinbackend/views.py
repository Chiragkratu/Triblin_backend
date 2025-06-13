from rest_framework import generics, permissions
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, PlasticItemSerializer, LocationItemSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlasticItemSerializer
from rest_framework.views import APIView
from .models import Messages,location_count, PlasticItem,Location, Plastic_Item, AuthUser, Plastic_Item_Replacement
from .serializers import MessagesSerializer
from django.core.mail import send_mail
from django.conf import settings


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

    def delete(self,request,itemid):
        username = request.user.username 
        data = request.data 
        try:
            item = PlasticItem.objects.get(item_id=itemid, username=username)
        except PlasticItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if item.quantity == "0":
            item.delete()
            return

        if int(item.quantity) >= int(data.get('quantity')):
            
            item.quantity= str(int(item.quantity)-int(data.get("quantity")))
            item.save()
        else:
            return Response({"error": "BAD REQUEST"}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, itemid):
        user_id = request.user.id
        data = request.data
        location_id = data.get("location")

        try:
        # Step 1: Get the Plastic_Item owned by this user
             item = Plastic_Item.objects.get(id=itemid, user_id=user_id)
        except Plastic_Item.DoesNotExist: 
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Get replacement quantity
        replacement_quantity = int(data.get("quantity"))

        # Step 3: Check available quantity
        if item.quantity == 0:
            return Response({"error": "No quantity available to replace"}, status=status.HTTP_400_BAD_REQUEST)

        if item.quantity < replacement_quantity:
            return Response({"error": "Not enough quantity to replace"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Reduce item quantity and save
        item.quantity -= replacement_quantity
        item.save()

        # Step 5: Create replacement entry
        try:
            Plastic_Item_Replacement.objects.create(
                plastic_name=item,  # Already retrieved
                location_name=Location.objects.get(id=location_id),
                replaced_with=data.get("itemreplace"),
                quantity=replacement_quantity,
                date=data.get("date"),
                disposed_type=data.get("disposedtype"),
                user=AuthUser.objects.get(id=user_id),
            )
        except Exception as e:
            return Response({"error": f"Replacement creation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Replacement recorded successfully."}, status=status.HTTP_200_OK)
class PlasticItemListView(APIView):

    def post(self, request):
        user_id = request.user.id
        data = request.data.copy()
        print(data)
        data['user'] = AuthUser.objects.get(id=user_id)
        location_obj = Location.objects.get(id=data['location_name'])
        data['location_name'] = location_obj
        print(data)
        item = Plastic_Item.objects.filter(location_name=location_obj, user=data['user'], plastic_type=data['plastic_type']).first()
        print(item)
        if item:
            newquantity = int(item.quantity)+int(data['quantity'])
            print(item.quantity)
            item.quantity=newquantity
            item.save()
            return Response({'object updated successfully'},status=status.HTTP_200_OK)
        else:
            Plastic_Item.objects.create(**data)
            return Response({'object added successfully'},status=status.HTTP_200_OK)
            
    def get(self, request):
        user_id = request.user.id
        if user_id is not None:
            items = Plastic_Item.objects.filter(user=user_id)
            serializer = PlasticItemSerializer(items, many=True)
            return Response(serializer.data)
        return Response({'error': 'Username parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class MessagesView(APIView):
    def post(self, request):
        serializer = MessagesSerializer(data=request.data)
        data = request.data
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Roomview(APIView):
    def post(self, request):
        userid = request.user.id
        room = request.data.get('room')
        entryitem = location_count.objects.filter(location_name=room, user_id=userid).first()
        if entryitem:
            entryitem.location_count += 1
            entryitem.save()
            new_room_name = f"{room}{entryitem.location_count}"
        else:
            location_count.objects.create(location_name=room, location_count=1, user_id=userid)
            new_room_name = f"{room}1"

        Location.objects.create(location_name=new_room_name, user_id=userid)

        return Response({"message": f"Location '{new_room_name}' created."}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.user.id
        items = Location.objects.filter(user_id=user_id).all()

        serializer = LocationItemSerializer(items,many=True)
        return Response(serializer.data)




                
                


