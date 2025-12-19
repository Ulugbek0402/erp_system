from rest_framework.generics import CreateAPIView

from erp.models import Student
from erp.permissions import IsStudent
from erp.serializers.serializers import StudentSerializer


class StudentAPI(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

