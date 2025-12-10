from idlelib.query import CustomRun

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from erp.models import *
from erp.serializers import *


# @swagger_auto_schema(
#     method='get',
#     responses={200: ActorSerializer(many=True)}
# )
# @swagger_auto_schema(
#     method='post',
#     request_body=ActorSerializer,
#     responses={201: ActorSerializer()}
# )
# @api_view(['GET', 'POST'])
# def actor_get_post(request):
#
#     if request.method == 'GET':
#         actors = Actor.objects.all()
#         serializer = ActorSerializer(actors, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         serializer = ActorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ActorApi(APIView):

    @swagger_auto_schema(request_body=ActorSerializer)
    def post(self, request):
        serializer = ActorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ActorDetailApi(APIView):

    def get(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializer(actor)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializer(actor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"key": "value"}, status=status.HTTP_201_CREATED)

# @swagger_auto_schema(
#     method='get',
#     responses={200: MovieSerializer(many=True)}
# )
# @swagger_auto_schema(
#     method='post',
#     request_body=MovieSerializer,
#     responses={201: MovieSerializer()}
# )
# @api_view(['GET', 'POST'])
# def movie_get_post(request):
#
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class MovieApi(APIView):
#
#     @swagger_auto_schema(request_body=MovieSerializer)
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#     @swagger_auto_schema(responses={200: MovieSerializer(many=True)})
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#
# class MovieDetailApi(APIView):
#     def get(self, request, slug):
#         #actor = get_object_or_404(Actor, slug=slug)
#         movie = Movie.objects.get(slug=slug)
#         serializer = MovieSerializer(movie)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, slug):
#         actor = get_object_or_404(Actor, slug=slug)
#         serializer = MovieSerializer(actor, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)

# class CommitApi(APIView):
#
#     @swagger_auto_schema(request_body=CommitSerializer)
#     def post(self, request):
#         serializer = CommitSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#     @swagger_auto_schema(responses={200: CommitSerializer(many=True)})
#     def get(self, request):
#         coms = CommitMovie.objects.all()
#         serializer = CommitSerializer(coms, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

class CommitApi(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {"success": True}
        commits = CommitMovie.objects.filter(author=request.user)
        serializer = CommitSerializer(commits, many=True)
        response["data"] = serializer.data
        return Response(data=response)

    @swagger_auto_schema(request_body=CommitSerializer)
    def post(self, request):
        response = {"success": True}
        serializer = CommitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            response["data"] = serializer.data
            return Response(data=response)
        return Response(data=serializer.data)


class MovieModelViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #pagination_class = CustomPagination

# class CommitApi(ModelViewSet):
#     queryset = CommitMovie.objects.all()
#     serializer_class = CommitSerializer

@action(detail=True, methods=['POST'])
def add_actor(self, request, *args, **kwargs):
    actor_id = request.data['actor_id']
    movie = self.get_object()
    movie.actor.add(actor_id)
    movie.save()

    serializer = MovieSerializer(movie)
    return Response(data=serializer.data)
