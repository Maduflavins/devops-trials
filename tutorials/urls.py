from django.urls import path
from tutorials import views 
 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tutorials', views.TutorialViewSet)

app_name = 'tutorials'

urlpatterns = [
    path('', include(router.urls))
]