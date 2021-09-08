from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = ('__all__')
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = (
            'post',
            'created',
        )


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        follow_obj = data['following']
        if user == follow_obj:
            raise serializers.ValidationError(
                'Подписываться на себя нельзя!'
            )
        if Follow.objects.filter(
            user=User.objects.get(username=user),
            following=User.objects.get(username=follow_obj)
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписались'
            )
        return data
