from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from .views import UserViewSet, ContentAPIView, ContentDetailsView

user_router = routers.DefaultRouter()

user_router.register(r'users', UserViewSet, 'User')
# user_router.register(r'content', ContentAPIView.as_view(), basename='content')
# user_router.register(r'details', ContentDetailsView.as_view(), basename='details')

urlpatterns = [
    path('',include(user_router.urls)),
    path('content/', ContentAPIView.as_view()),
    path('details/<int:pk>/', ContentDetailsView.as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)
