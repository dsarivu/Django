from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, get_destinations, incoming_data
from .views import home

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('home', home, name='home'),
    path('', include(router.urls)),
    path('get_destinations/<uuid:account_id>/', get_destinations),
    path('server/incoming_data/', incoming_data),
]
