"""View module for handling requests about voices"""
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from serverapi.models import Voice, Text, Category

class Voices(ViewSet):

    # It feels like I'll never finish this component.

    def create(self, request):
        """Handle POST operations for adding a voice
        
        Returns:
            Response -- JSON serialized voice instance
        """

        voice = Voice()
        voice.name = request.data["name"]
        voice.create_date = request.data["create_date"]
        voice.recording = request.data["recording"]
        voice.edited = request.data["edited"]
        voice.privacy = request.data["privacy"]
        token = Token.objects.get(user=request.auth.user)
        voice.creator_id = token
        category = Category.objects.get(pk=request.data["category_id"])
        voice.category = category
        text = Text.objects.get(pk=request.data["text_id"])
        voice.text = text

        try:
            voice.save()
            serializer = VoiceSerializer(voice, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single Voice """

        try:
            voice = Voice.objects.get(pk=pk)
            serializer = VoiceSerializer(voice, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """ update/ edit an existing Voice """


        voice = Voice.objects.get(pk=pk)
        voice.name = request.data["name"]
        voice.create_date = request.data["create_date"]
        voice.recording = request.data["recording"]
        voice.edited = request.data["edited"]
        voice.privacy = request.data["privacy"]
        voice.creator = voice.creator
        category = Category.objects.get(pk = request.data["category_id"])
        voice.category_id = category
        text = Text.objects.get(pk=request.data["text_id"])
        voice.text_id = text
        voice.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing Voice """

        try:
            voice = Voice.objects.get(pk=pk)
            voice.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Voice.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        "GET all Voices"
        voices = Voice.objects.all()

        serializer = VoiceSerializer(voices, many=True, context={'request': request})
        return Response(serializer.data)

class VoiceSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voices """

    class Meta:
        model = Voice
        fields = ('id', 'name', 'create_date', 'recording', 'edited', 'privacy', 'creator_id', 'category_id', 'text_id')
        depth = 2
