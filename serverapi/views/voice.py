"""View module for handling requests about voices"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from serverapi.models import Voice, Birdie, Category, BirdieVoice


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
        fields = ('id', 'label')

class VoiceSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voices """
    creator = BirdieSerializer(many=False)
    voice_category = CategorySerializer

    class Meta:
        model = Voice
        fields = ('id', 'voice_name', 'date_created', 'creator', 'category', 'voice_text', 'last_edit', 'privacy')
        depth = 1

class Voices(ViewSet):
    """ comments for Voicecatcher """

    def create(self, request):
        """ POST operations for adding a Voice """

        voice = Voice()
        voice.voice_name = request.data['voice_name']
        voice.date_created = request.data['date_created']
        voice.creator = Birdie.objects.get(user=request.auth.user)
        voice.category = Category.objects.get(pk=request.data['category_id'])
        voice.voice_text = request.data['voice_text']
        voice.last_edit = request.data['last_edit']

        try:
            voice.save()
            serializer = VoiceSerializer(voice, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

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

    def list(self, request):
        """Handle GET requests to voices resource
        
        Returns:
            Response -- JSON serialized list of voices
        """
        birdie = Birdie.objects.get(birdie=request.auth.user)
        voices = Voice.objects.all()

        # Set the `privacy` property on every voice
        for voice in voices:
            voice.privacy = None

            try:
                BirdieVoice.objects.get(voice=voice, birdie=birdie)
                voice.privacy = True
            except BirdieVoice.DoesNotExist:
                voice.privacy = False

        # Support filtering voices by category
        category = self.request.query_params.get('categoryId', None)
        if category is not None:
            voices = voices.filter(category__id=type)

        serializer = VoiceSerializer(
            voices, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def voice_privacy(self, request, pk=None):
        """Managing voices being private or public"""

        # A Birdie wants to set the voice privacy
        if request.method == "POST":
            # The pk would be `2` if the URL above was requested
            voice = Voice.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which birdie is making the request for privacy
            birdie = Birdie.objects.get(user=request.auth.user)

            try:
                # Determine if the voice is already private
                privacy_check = BirdieVoice.objects.get(
                    voice=voice, birdie=birdie)
                return Response(
                    {'message': 'Birdie already signed up this Voice.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except BirdieVoice.DoesNotExist:
                # The user is not signed up.
                privacy_check = BirdieVoice()
                privacy_check.voice = voice
                privacy_check.birdie = birdie
                privacy_check.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to make a voice public
        elif request.method == "DELETE":
            # Handle the case if the client specifies a game
            # that doesn't exist
            try:
                voice = Voice.objects.get(pk=pk)
            except Voice.DoesNotExist:
                return Response(
                    {'message': 'Voice does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authenticated user
            birdie = Birdie.objects.get(user=request.auth.user)

            try:
                # Try to delete the signup
                privacy_check = BirdieVoice.objects.get(
                    voice=voice, birdie=birdie)
                privacy_check.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except BirdieVoice.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for Voice.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)