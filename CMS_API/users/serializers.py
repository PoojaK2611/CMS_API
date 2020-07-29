from .models import Content, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'pincode']


class ContentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Content
        fields = ['title', 'body', 'summary', 'category', 'document', 'author']

    def create(self, validated_data):
        validated_data["author"] = self.context.get('request').user
        return super().create(validated_data)

