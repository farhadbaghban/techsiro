from rest_framework import serializers
from projectApps.comments.models import Comment


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["product", "content", "response", "is_response"]


class CommentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "product",
            "content",
            "created_at",
            "response",
            "is_response",
        ]
