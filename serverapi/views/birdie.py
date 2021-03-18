import uuid
import base64
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.files.base import ContentFile
from serverapi.models import Voice, Birdie, VoiceCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username', 'email')

class BirdieSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False)

    class Meta:
        model = Birdie
        fields = ('id', 'bio', 'user_id')
        # depth = 1

class Birdies(ViewSet):
    """ comments for dreamcatcher """

    def retrieve(self, request, pk=None):
        """ get a single Birdie """

        try:
            birdie = Birdie.objects.get(pk=pk)

            serializer = BirdieSerializer(birdie, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all Birdies"
        birdie = Birdie.objects.all()
        
        serializer = BirdieSerializer(birdie, many=True, context={'request': request})

        return Response(serializer.data)
