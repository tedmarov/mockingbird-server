"""View module for handling requests about voices"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from serverapi.models import Voice, Birdie, Text, Category, BirdieText

class UserSerializer(serializers.ModelSerializer):
    """ JSON serializer for user """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class BirdieSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Birdie """
    user = UserSerializer(serializers.ModelSerializer)
    class Meta:
        model = Birdie
        fields = ('id', 'user', 'bio')

class CategorySerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voice type """
    class Meta:
        model = Category
        fields = ('id', 'category_label')

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('text_title', 'submitter', 'edited_on', 'text_body', 'text_source')

class VoiceSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voices """
    category = CategorySerializer(serializers.ModelSerializer)
    text = TextSerializer(serializers.ModelSerializer)
    class Meta:
        model = Voice
        fields = ('id', 'voice_name', 'date_created', 'creator', 'category', 'voice_recording', 'text', 'voice_edited', 'privacy')
        depth = 2


class BirdieTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdieText
        fields = ('bio', 'user', 'text_title', 'submitter', 'edited_on', 'text_body', 'text_source')
        depth = 2

class Voices(ViewSet):

    def list(self, request):
        "GET all Voices"
        voices = Voice.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            voices = voices.filter(user_id=user_id)
        
        serializer = VoiceSerializer(voices, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        """ POST operations for adding a Voice """

        voice = Voice()
        voice.voice_name = request.data['voice_name']
        voice.date_created = request.data['date_created']
        voice.creator = Birdie.objects.get(user=request.auth.user)
        voice.recording = request.data['voice_recording']
        voice.category = Category.objects.get(pk=request.data['category_id'])
        voice.voice_text = request.data['voice_text']
        voice.last_edit = request.data['last_edit']

        try:
            voice.save()
            serializer = VoiceSerializer(voice, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

# Create Custom Action to add to MtoM table?
    @action(methods=['post', 'delete'], detail=True)
    def modifyBirdieText(self, request, pk=None):
        """Managing multiple birdies having multiple texts"""

        # A birdie just recorded the voice and wants to post
        if request.method == "POST":
            # The pk would depend
            text = Text.objects.get(pk=pk)

            # Django uses Auth header to figure out
            # the birdie that posted
            birdie = Birdie.objects.get(user=request.auth.user)

            try:
                # Was this recording already made?
                recording = BirdieText.objects.get(
                    text=text, birdie=birdie)
                return Response(
                    {'message': 'Birdie already posted this voice recording.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except BirdieText.DoesNotExist:
                # The BirdieText instance does not exist
                recording = BirdieText()
                recording.text = text
                recording.birdie = birdie
                recording.save()

                return Response({}, status=status.HTTP_201_CREATED)
            
        # Voice is to be deleted
        elif request.method == "DELETE":
            # Handle the case if the birdie specifies a non-existing object
            try:
                text = Text.objects.get(pk=pk)
            except Text.DoesNotExist:
                return Response(
                    {'message': 'Text no longer exists in the system.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the auth user
            birdie = Birdie.objects.get(user=request.auth.user)

            try:
                # Try to delete the BirdieText
                recording = BirdieText.objects.get(
                    text=text, birdie=birdie)
                recording.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            
            except BirdieText.DoesNotExist:
                return Response(
                    {'message': 'Birdie already deleted this voice recording'}
                )

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

        voice.voice_name = request.data['voice_name']
        voice.date_created = request.data['date_created']
        voice.creator = Birdie.objects.get(user=request.auth.user)
        voice.voice_recording = request.data['voice_recording']
        voice.category = Category.objects.get(pk=request.data['category_id'])
        voice.voice_text = request.data['voice_text']
        voice.last_edit = request.data['last_edit']

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

