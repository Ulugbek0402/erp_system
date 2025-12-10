from rest_framework import serializers

from erp.models import Actor, Movie, CommitMovie


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(many=True)
    class Meta:
        model = Movie
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'genre', 'actor']
        read_only_fields = ['slug']


class CommitSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommitMovie
        fields = ['id', 'title', 'author', 'movie']
        read_only_fields = ['author']
