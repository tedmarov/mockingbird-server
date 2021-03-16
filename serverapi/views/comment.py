from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from serverapi.models import Comment, Birdie, Voice

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'comment_title', 'author_id', 'created_on', 'voice', 'comment_detail', 'last_edit')
        depth = 1

class Comments(ViewSet):
    """ comments for dreamcatcher """

    def create(self, request):
        """ POST operations for adding comments """

        commenter = Birdie.objects.get(user=request.auth.user)

        comment = Comment()

        comment.comment_detail = request.data['comment_detail']

        voice = Voice.objects.get(pk=request.data["voice_id"])

        comment.author = commenter

        comment.voice = voice

        try:
            comment.save()

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ get a single comment """

        try:
            comment = Comment.objects.get(pk=pk)

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        "GET all comments"
        comments = Comment.objects.all()
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """ update/ edit an existing comment """

        commenter = Birdie.objects.get(user=request.auth.user)
        comment = Comment.objects.get(pk=pk)

        comment.comment_detail = request.data['comment_detail']
        comment.created_on = request.data['created_on']
        voice = Voice.objects.get(pk=request.data["voice_id"])
        
        comment.author = commenter
        comment.voice = voice

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ deletes an existing comment """

        try:
            comment = Comment.objects.get(pk=pk)

            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'mesage': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

