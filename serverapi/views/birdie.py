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
from serverapi.models import Voice, Birdie, Category, Text, BirdieText  

# Don't return ID, security purposes
# Add in 'User' field in Birdie Serializer
# Create var in Serializer, line 24

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff', 'username', 'email')

class BirdieSerializer(serializers.ModelSerializer):
    # Whenever Birdie retrieved; USerializer will be invoked to grab USerializer fields
    # In order to get user info, just fetch the Birdie
    user = UserSerializer(many=False)

    class Meta:
        model = Birdie
        fields = ('bio', 'user')
        depth = 1

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('text_title', 'submitter', 'edited_on', 'text_body', 'text_source')

class BirdieTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdieText
        fields = ('bio', 'user', 'text_title', 'submitter', 'edited_on', 'text_body', 'text_source')

class Birdies(ViewSet):
    """ get a single Birdie """
    def retrieve(self, request, pk=None):

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
