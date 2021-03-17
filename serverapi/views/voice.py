from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from serverapi.models import Voice, Birdie, VoiceCategory
from django.contrib.auth.models import User


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

class VoiceCategorySerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voice type """
    class Meta:
        model = VoiceCategory
        fields = ('id', 'label')

class VoiceSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voices """
    creator = BirdieSerializer(many=False)
    voice_category = VoiceCategorySerializer

    class Meta:
        model = Voice
        fields = ('id', 'voice_name', 'date_created', 'creator', 'category', 'voice_text', 'last_edit')
        depth = 1

class Voices(ViewSet):
    """ comments for Voicecatcher """

    def create(self, request):
        """ POST operations for adding a Voice """

        voice = Voice()
        voice.voice_name = request.data['voice_name']
        voice.date_created = request.data['date_created']
        voice.creator = Birdie.objects.get(user=request.auth.user)
        voice.category = VoiceCategory.objects.get(pk=request.data['category_id'])
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

    def list(self, request):
        "GET all Voices"
        voices = Voice.objects.all()

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            voices = voices.filter(user_id=user_id)
        
        serializer = VoiceSerializer(voices, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing Voice """

        voice = Voice.objects.get(pk=pk)

        voice.voice_name = request.data['voice_name']
        voice.date_created = request.data['date_created']
        voice.creator = Birdie.objects.get(user=request.auth.user)
        voice.category = VoiceCategory.objects.get(pk=request.data['category_id'])
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
