
from rest_framework import viewsets, status, permissions
from .models import User, Content
from .serializers import UserSerializer, ContentSerializer
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=["POST"])
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
                serializer = UserSerializer(user)
                token = Token.objects.filter(user=user).first()
                if not token:
                    Token.objects.create(user=user)
                    print(token.key)
                    token=Token.objects.filter(user=user).first()
                response_data = serializer.data
                response_data['token']=token.key
                login(request,user)
            return Response(response_data)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
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


class ContentAPIView(APIView):
    """
    List all Contents and create new content
    """
    def get(self,request, format=None):
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentDetailsView(APIView):
    """
    Retrieve , Update and Delete Content instance
    """
    def get_object(self,pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permission_classes((permissions.IsAuthenticated,))
    def get(self,request,pk, format=None):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    @permission_classes((permissions.IsAuthenticated,))
    def put(self,request, pk, format=None):
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data)
        """"
        Check whether user is authorized to update
        """
        user = request.user
        if content.user != user:
            return Response({"detail": "You don't have permission to edit that."})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((permissions.IsAuthenticated,))
    def delete(self,request, pk, format=None):
        content = self.get_object(pk)
        """"
          Check whether user is authorized to update
        """
        user = request.user
        if content.user != user:
            return Response({"detail": "You don't have permission to delete that."})

        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

