from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from kinoteatr.views import *


urlpatterns = [
    #path('actor/', actor_get_post),
    path('actor/', ActorApi.as_view()),
    #path('movies/', movie_get_post),
    # path('movie/', MovieApi.as_view()),
    path('actor/<int:pk>/', ActorDetailApi.as_view()),
    # path('movie/<int:slug>/>', MovieDetailApi.as_view()),
    #path('movie/<int:pk>/>', MovieApi.as_view()),
    path('commit/', CommitApi.as_view()),
    path('auth/', obtain_auth_token)
]
