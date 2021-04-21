from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from serverapi.models import Voice, Text, Category

# class UserSerializer(serializers.ModelSerializer):
#     """ JSON serializer for user """
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'username')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'category_label')

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('text_id', 'text_title', 'submitter', 'text_body', 'text_source')

class VoiceSerializer(serializers.ModelSerializer):
    """ JSON Serializer for Voices """
    # category = CategorySerializer(serializers.ModelSerializer)
    # text = TextSerializer(serializers.ModelSerializer)
    class Meta:
        model = Voice
        fields = ('id', 'name', 'created', 'creator_id', 'recording', 'category_id', 'text_id', 'edited', 'privacy')
        depth = 2

class Voices(ViewSet):

    def list(self, request):
        "GET all Voices"
        voices = Voice.objects.all()

        serializer = VoiceSerializer(voices, many=True, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ get a single Voice """

        try:
            voice = Voice.objects.get(pk=pk)
            serializer = VoiceSerializer(voice, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """ POST operations for adding a Voice """


        voice = Voice()
        voice.creator_id = Token.objects.get(user=request.auth.user)
        voice.name = request.data["name"]
        voice.created = request.data["created"]
        voice.edited = False
        voice.privacy = request.data["privacy"]
        voice.recording = request.data["recording"]
        print(request.data['category_id'])
        voice.category_ids = Category.objects.get(pk=request.data["category_id"])
        voice.text_id = Text.objects.get(pk=request.data["text_id"])


        try:
            voice.save()
            serializer = VoiceSerializer(voice, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """ update/ edit an existing Voice """


        voice = Voice.objects.get(pk=pk)
        voice.name = request.data["name"]
        voice.created = request.data["created"]
        voice.recording = request.data["recording"]
        voice.edited = True
        voice.privacy = request.data["privacy"]
        user = Token.objects.get(user=request.auth.user)
        category = Category.objects.get(pk = request.data["category_id"])
        text = Text.objects.get(pk = request.data["text_id"])
        voice.creator = user
        voice.category_id = category
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



# class BirdieTextSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BirdieText
#         fields = ('bio', 'user', 'text_title', 'submitter', 'text_body', 'text_source')
#         depth = 2

# # Create Custom Action to add to MtoM table?
#     @action(methods=['post', 'delete'], detail=True)
#     def modifyBirdieText(self, request, pk=None):
#         """Managing multiple birdies having multiple texts"""

#         # A birdie just recorded the voice and wants to post
#         if request.method == "POST":
#             # The pk would depend
#             text = Text.objects.get(pk=pk)

#             # Django uses Auth header to figure out
#             # the birdie that posted
#             birdie = Birdie.objects.get(user=request.auth.user)

#             try:
#                 # Was this recording already made?
#                 recording = BirdieText.objects.get(
#                     text=text, birdie=birdie)
#                 return Response(
#                     {'message': 'Birdie already posted this voice recording.'},
#                     status=status.HTTP_422_UNPROCESSABLE_ENTITY
#                 )
#             except BirdieText.DoesNotExist:
#                 # The BirdieText instance does not exist
#                 recording = BirdieText()
#                 recording.text = text
#                 recording.birdie = birdie
#                 recording.save()

#                 return Response({}, status=status.HTTP_201_CREATED)
            
#         # Voice is to be deleted
#         elif request.method == "DELETE":
#             # Handle the case if the birdie specifies a non-existing object
#             try:
#                 text = Text.objects.get(pk=pk)
#             except Text.DoesNotExist:
#                 return Response(
#                     {'message': 'Text no longer exists in the system.'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Get the auth user
#             birdie = Birdie.objects.get(user=request.auth.user)

#             try:
#                 # Try to delete the BirdieText
#                 recording = BirdieText.objects.get(
#                     text=text, birdie=birdie)
#                 recording.delete()
#                 return Response(None, status=status.HTTP_204_NO_CONTENT)
            
#             except BirdieText.DoesNotExist:
#                 return Response(
#                     {'message': 'Birdie already deleted this voice recording'}
#                 )
