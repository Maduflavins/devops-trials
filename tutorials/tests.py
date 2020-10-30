from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from . models import Tutorial

from . serializers import TutorialSerializer

TUTORIAL_URL = reverse('tutorials:tutorial-list')


class PublicTutorialApiTests(TestCase):
    """Test that registration is not required for creating, listing or deleting tutorial"""

    # def setUp(self):
    #     self.user = get_user_model().objects.create_user(
    #         "test@test.com",
    #         "password@123"
    #     )
    #     self.client = APIClient()
    #     self.client.force_authenticate(self.user)

    
    def test_retrieve_tutorials(self):
        """Test retrieving tutorial"""
        Tutorial.objects.create(title="movement in the logs", description="this is a lot of way to do something", published=True)
        Tutorial.objects.create(title="water man", description="can you make things happen", published=True)

        res = self.client.get(TUTORIAL_URL)
 
        tutorials = Tutorial.objects.all().order_by('-title')
        serializer = TutorialSerializer(tutorials, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {"title":"movement in the logs", "description":"this is a lot of way to do something", "published":True}
        res=self.client.post(TUTORIAL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

