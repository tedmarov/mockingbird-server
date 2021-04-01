from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from serverapi.models import Text

class Texts(ViewSet):

    def list(self, request):

        texts = Text.objects.all()

        serializer = TextSerializer(texts, many=True, context={'request', request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            text = Text.objects.get(pk=pk)
            serializer = TextSerializer(text, context={'request', request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):

        text = Text()
        text.text_title = request.data["text_title"]
        text.submitter = Token.objects.get(user=request.auth.user)
        text.text_body = request.data["text_body"]
        text.text_source = request.data["text_source"]

        try:
            text.save()
            serializer = TextSerializer(text, context={'request', request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        text = Text.objects.get(pk=pk)
        text.text_title = request.data["text_title"]
        text.submitter = Token.objects.get(user=request.auth.user)
        text.text_body = request.data["text_body"]
        text.text_source = request.data["text_source"]

        text.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            text = Text.objects.get(pk=pk)
            text.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Text.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text

        fields = ('id', 'text_title', 'submitter', 'text_body', 'text_source')
        depth = 2
