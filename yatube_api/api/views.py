from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnlyPermission, IsUserAuthPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer,
)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsUserAuthPermission,)
    http_method_names = ('get', 'post')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def perform_create(self, serializer):
        user = self.request.user
        follow_obj = serializer.initial_data.get('following')
        if user.username == follow_obj:
            raise PermissionDenied('Невозможно подписаться на самого себя')
        elif Follow.objects.filter(
            user=user,
            following=User.objects.get(username=follow_obj)
        ).exists():
            raise ParseError('Вы уже подписаны')
        elif serializer.is_valid():
            serializer.save(user=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_queryset(self):
        return Follow.objects.filter(
            user__username=self.request.user.username
        )
