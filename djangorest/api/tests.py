from django.test import TestCase
#from .models import Recommendation, User
from django.contrib.auth.models import User
from .models import Recommendation

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
# Create your tests here.

class ModelTestCase(TestCase):
    """This class defines the test suite for the recommendation model."""


    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create(username="nerd") # ADD THIS LINE
        self.title = "Write world class code"
        # specify owner of a bucketlist
        self.recommendation = Recommendation(title=self.title, owner=self.user) # EDIT THIS TOO
    
    # def setUp(self):
    #     """Define the test client and other test variables."""
    #     self.title = "Test Recommendation"
    #     self.username = "TestUser"
    #     self.user = User(username="TestUser")


    def test_model_can_create_user_and_a_recommendation(self):
        """Test the Recommendation model can create a recommendation."""

        old_count = Recommendation.objects.count()
        self.recommendation.save()
        new_count = Recommendation.objects.count()
        self.assertNotEqual(old_count, new_count)


# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""

        self.user = User.objects.create(username="nerd") # ADD THIS LINE

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.title = "Write world class code"

        #self.recommendation = Recommendation(title=self.title)

        self.recommendation_data = {'title': 'Go to Ibiza', 'comment': 'Go to Ibiza' ,'reference': 'Go to Ibiza','owner': self.user.id}
        self.response = self.client.post(
            reverse('create'),
            self.recommendation_data,
            format="json")

        self.recommendation = Recommendation.objects.get(title='Go to Ibiza')

    def test_api_can_create_a_recommendation(self):
        """Test the api has recommendation creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    def test_api_can_get_a_recommendation(self):
        """Test the api can get a given recommendation."""
        recommendation = Recommendation.objects.get()
        response = self.client.get(
            '/recommendation/',
            kwargs={'pk': recommendation.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, recommendation)

    def test_api_can_delete_recommendation(self):
        """Test the api can delete a recommendation."""
        #recommendation = Recommendation.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': self.recommendation.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_api_can_update_recommendation(self):
        """Test the api can update a given recommendation."""
        #recommendation = Recommendation.objects.get()
        change_recommendation = {'title': 'Go to Ibiza', 'comment': 'Go to Ibiza' ,'reference': 'Go to Ibiza'}
        res = self.client.put(
            reverse('details', kwargs={'pk': self.recommendation.id}),
            change_recommendation, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/recommendation/', kwargs={'pk': 1}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
