from rest_framework import serializers

from erp.models import *


class SendEmail(serializers.Serializer):
    text = serializers.CharField()
    email = serializers.EmailField()


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdminUser
#         fields = "__all__"