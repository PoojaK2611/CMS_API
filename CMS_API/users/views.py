
from .models import User, Content
from .serializers import UserSerializer, ContentSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import filters
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=["POST"], permission_classes=[~IsAuthenticated])
    def login_with_password(self,request):
        try:
            email = request.data.get('email')
            if not email:
                return Response({'detail':'Please provide email.'}, status=status.HTTP_400_BAD_REQUEST)
            password = request.data.get('password')
            if not password:
                return Response({'detail': 'Please provide password.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = User.objects.get(email=email, is_active=True)
                except User.DoesNotExist:
                    return Response({'detail':'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                if not user or not user.password:
                    return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
                logger.info(password + ' - ' + user.password)
                if not check_password(password, user.password):
                    return Response({'detail': 'Unauthorised'}, status=401)

                serializer = UserSerializer(user)
                token = Token.objects.filter(user=user).first()
                if not token:
                    Token.objects.create(user=user)
                    print(token.key)
                    token=Token.objects.filter(user=user).first()

                response_data = serializer.data
                response_data['token']= token.key
                login(request,user)
            return Response(response_data)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def logout(self,request):
        try:
            if request.user:
                print('Logging out '+ request.user.email)
                logout(request)
                return Response({'detail': 'Logged out.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Error':'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    """
        Search functionality 
    """
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'summary', 'category']

    def get_queryset(self):
        return Content.objects.all()
