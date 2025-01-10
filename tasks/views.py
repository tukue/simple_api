# tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TaskAPIView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
