from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from serverapi.models import Category, Birdie, Voice
from datetime import datetime

class Categories(ViewSet):

    def list(self, request):

        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True, context={'request', request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request', request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):

        user = Token.objects.get(user=request.auth.user)
        voice = Voice.objects.get(pk = request.data['voice_id'])

        category = Category()
        category.category_label = request.data['category_title']

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request', request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        user = Token.objects.get(user=request.auth.user)

        category = Category.objects.get(pk=pk)
        category.category_label = request.data['category_title']

        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category

		fields = ['label']
		depth = 1

