from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)
router_v1.register(
    r'follow', FollowViewSet, basename='follow'
)
v1_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
