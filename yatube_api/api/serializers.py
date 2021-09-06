from django.contrib.auth import get_user_model
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author',
            'group',
            'image',
            'pub_date',
        )
        read_only_fields = (
            'author',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created',
        )
        read_only_fields = (
            'author',
            'post',
            'created',
        )


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['user', 'following']
            )
        ]

    user = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()
        )
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    
    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Подписываться на себя нельзя!'
            )
        return data
