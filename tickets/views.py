from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from tickets.forms import TaskForm, LoginForm
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from tickets.auth import authentificate

# Create your views here.

class LoginAPIView(APIView):

    def post(self, request):

        data = request.POST

        username = data.get('username', None)

        password = data.get('password', None)

        if username is None or password is None:

            return Response({'error': 'Нужен и логин, и пароль'},

                            status=status.HTTP_400_BAD_REQUEST)

        user = authentificate(username, password)

        if user is None:

            return Response({'error': 'Неверные данные'},

                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        refresh.payload.update({

            'user_id': user.id,

            'username': user.username

        })

        return Response({

            'refresh': str(refresh),

            'access': str(refresh.access_token),

        }, status=status.HTTP_200_OK)
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'tickets/login.html', {'form': form})