from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url('^', include((router.urls, 'users')))
]
