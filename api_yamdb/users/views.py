from api.permissions import AdminOnly
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import service
from .models import User
from .serializers import (GetTokenSerializer, RegistrationSerializer,
                          UserSerializer)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user = User.objects.filter(email=email, username=username).first()
        if not user:
            user = serializer.save()
        code = user.set_confirmation_code()
        service.send_confirmation_code(user.email, code['code'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = {"token": serializer.data['token']}
        return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'

    @action(detail=False,
            methods=['get', 'put', 'patch'],
            permission_classes=(IsAuthenticated,)
            )
    def me(self, request, pk=None):
        user = request.user
        if request.method in ('PUT', 'PATCH'):
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if not request.user.is_admin:
                serializer.save(role=user.role)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data)
