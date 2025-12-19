from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from erp.models import Teacher
from erp.permissions import IsTeacher
from erp.serializers.serializers import TeacherSerializer


class SendEmailApi(APIView):
    #@swaggeauto_schema(request_body=SendEmail)
    def post(self, request):
        subject = "tema"
        message = request.data["text"]
        email = request.data["email"]
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f"{email}"]

        send_mail(subject, message, email_from, recipient_list)
        return Response(data=[f"{email}: yuborildi"])


class TeacherAPI(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacher]
