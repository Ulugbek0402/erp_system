from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, News, Commit
from .serializers import UserSerializer, CategorySerializer, NewsSerializer, CommitSerializer
from .permissions import IsAdmin, CommitRolePermission

User = get_user_model()


class UserListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        qs = User.objects.all().order_by("-id")
        data = UserSerializer(qs, many=True).data
        return Response(data)

    def post(self, request):
        ser = UserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(UserSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        ser = UserSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(UserSerializer(obj).data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        ser = UserSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(UserSerializer(obj).data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Category.objects.all().order_by("-id")
        return Response(CategorySerializer(qs, many=True).data)

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

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(CategorySerializer(obj).data)

    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = CategorySerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data)

    def patch(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = CategorySerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data)

    def delete(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = News.objects.select_related("category").all().order_by("-id")
        return Response(NewsSerializer(qs, many=True).data)

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

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(NewsSerializer(obj).data)

    def put(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = NewsSerializer(obj, data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(NewsSerializer(obj).data)

    def patch(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        ser = NewsSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(NewsSerializer(obj).data)

    def delete(self, request, pk):
        if not (request.user.is_admin or request.user.is_staff):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, CommitRolePermission]

    def get(self, request):
        qs = Commit.objects.select_related("user", "news").all().order_by("-id")
        return Response(CommitSerializer(qs, many=True).data)

    def post(self, request):
        ser = CommitSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data, status=status.HTTP_201_CREATED)


class CommitDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, CommitRolePermission]

    def get_object(self, pk):
        return get_object_or_404(Commit.objects.select_related("user", "news"), pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(CommitSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        ser = CommitSerializer(obj, data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        ser = CommitSerializer(obj, data=request.data, partial=True, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CommitSerializer(obj).data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
