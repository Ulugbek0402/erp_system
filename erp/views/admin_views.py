from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AdminAPI(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
