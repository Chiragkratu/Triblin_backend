from django.urls import path 
from .views import RegisterAPI,LoginAPI,UserAPI,PlasticItemView,MessagesView,Roomview

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/plastic-items/', PlasticItemView.as_view(), name='plastic-items'),
    path('api/plastic-items/<str:itemid>/', PlasticItemView.as_view(), name='plastic-items'),
    path('api/message',MessagesView.as_view(),name='messageview'),
    path('api/room',Roomview.as_view(), name="Roomview")
]
