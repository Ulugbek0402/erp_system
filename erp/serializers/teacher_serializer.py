from rest_framework import serializers


class SendEmail(serializers.Serializer):
    text = serializers.CharField()
    email = serializers.EmailField()