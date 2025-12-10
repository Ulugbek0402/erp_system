from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

from erp.views import *


urlpatterns = [
    #path('actor/', actor_get_post),
    path('actor/', ActorApi.as_view()),
    #path('movies/', movie_get_post),
    # path('movie/', MovieApi.as_view()),
    path('actor/<int:pk>/>', ActorDetailApi.as_view()),
    # path('movie/<int:slug>/>', MovieDetailApi.as_view()),
    #path('movie/<int:pk>/>', MovieApi.as_view()),
    path('commit/', CommitApi.as_view()),
    path('auth/', obtain_auth_token)
]
