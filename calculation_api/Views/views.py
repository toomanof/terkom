from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthView(APIView):
    """
    Authentication is needed for this methods
    """

    def get(self, request, format=None):
        return Response({'detail': "GET Response"})

    def post(self, request, format=None):
        try:
            data = request.data

        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

        if "username" not in data or "password" not in data:
            return Response({
                'status': 'error',
                'description': "'username' or 'password' not in Body",
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return Response({
                'status': 'wrong',
                'description': 'No default user, please create one',

            }, status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get_or_create(user=user)

        return Response({'detail': 'POST answer', 'token': token[0].key})
