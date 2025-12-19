from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Category, News, Commit
from .serializers import (
    UserSerializer,
    CategorySerializer,
    NewsSerializer,
    CommitSerializer,
    LoginSerializer,
)
from .permissions import IsAdmin, CommitRolePermission

User = get_user_model()


class UserListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(tags=["app1/users"])
    def get(self, request):
        qs = User.objects.all().order_by("-id")
        return Response(UserSerializer(qs, many=True).data)

    @swagger_auto_schema(tags=["app1/users"], request_body=UserSerializer)
    def post(self, request):
        ser = UserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(tags=["app1/users"])
    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(UserSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/users"], request_body=UserSerializer)
    def put(self, request, pk):
        obj = self.get_object(pk)
        ser = UserSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(UserSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/users"], request_body=UserSerializer)
    def patch(self, request, pk):
        obj = self.get_object(pk)
        ser = UserSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(UserSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/users"])
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["app1/categories"])
    def get(self, request):
        qs = Category.objects.all().order_by("-id")
        return Response(CategorySerializer(qs, many=True).data)

    @swagger_auto_schema(tags=["app1/categories"], request_body=CategorySerializer)
    def post(self, request):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        ser = CategorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    @swagger_auto_schema(tags=["app1/categories"])
    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(CategorySerializer(obj).data)

    @swagger_auto_schema(tags=["app1/categories"], request_body=CategorySerializer)
    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = CategorySerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data)

    @swagger_auto_schema(tags=["app1/categories"], request_body=CategorySerializer)
    def patch(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = CategorySerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data)

    @swagger_auto_schema(tags=["app1/categories"])
    def delete(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["app1/news"])
    def get(self, request):
        qs = News.objects.select_related("category").all().order_by("-id")
        return Response(NewsSerializer(qs, many=True).data)

    @swagger_auto_schema(tags=["app1/news"])
    def post(self, request):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        ser = NewsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(NewsSerializer(obj).data, status=status.HTTP_201_CREATED)


class NewsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(News, pk=pk)

    @swagger_auto_schema(tags=["app1/news"])
    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(NewsSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/news"], request_body=NewsSerializer)
    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = NewsSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(NewsSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/news"], request_body=NewsSerializer)
    def patch(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = NewsSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(NewsSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/news"])
    def delete(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, CommitRolePermission]

    @swagger_auto_schema(tags=["app1/commits"])
    def get(self, request):
        qs = Commit.objects.select_related("user", "news").all().order_by("-id")
        return Response(CommitSerializer(qs, many=True).data)

    @swagger_auto_schema(tags=["app1/commits"], request_body=CommitSerializer)
    def post(self, request):
        ser = CommitSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data, status=status.HTTP_201_CREATED)


class CommitDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, CommitRolePermission]

    def get_object(self, pk):
        return get_object_or_404(Commit.objects.select_related("user", "news"), pk=pk)

    @swagger_auto_schema(tags=["app1/commits"])
    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(CommitSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/commits"], request_body=CommitSerializer)
    def put(self, request, pk):
        obj = self.get_object(pk)
        ser = CommitSerializer(obj, data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/commits"], request_body=CommitSerializer)
    def patch(self, request, pk):
        obj = self.get_object(pk)
        ser = CommitSerializer(obj, data=request.data, partial=True, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data)

    @swagger_auto_schema(tags=["app1/commits"])
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["app1/login"],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Token response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_admin": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "is_manager": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            401: openapi.Response(description="Unauthorized"),
        },
    )
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        username = ser.validated_data["username"]
        password = ser.validated_data["password"]

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Login yoki parol noto‘g‘ri"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
                "is_staff": user.is_staff,
                "is_manager": user.is_manager,
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["app1/login"])
    def post(self, request):
        # token yo'q bo'lsa xato chiqmasin
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)